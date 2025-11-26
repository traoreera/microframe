# microframework/docs/openapi.py
import inspect
import re
from typing import Any, Dict, List, Optional, get_args, get_origin

from microframe.routing.router import RouteInfo


class OpenAPIGenerator:
    """Générateur de documentation OpenAPI 3.0 avec support complet"""

    def __init__(
        self,
        routes: List[RouteInfo],
        title: str = "API",
        version: str = "1.0.0",
        description: str = "",
        contact: Optional[Dict[str, str]] = None,
        license_info: Optional[Dict[str, str]] = None,
    ):
        self.routes = routes
        self.title = title
        self.version = version
        self.description = description
        self.contact = contact
        self.license_info = license_info
        self.schemas: Dict[str, Any] = {}

    def generate(self) -> Dict[str, Any]:
        """Génère le schéma OpenAPI complet"""
        info = {
            "title": self.title,
            "version": self.version,
            "description": self.description,
        }

        if self.contact:
            info["contact"] = self.contact

        if self.license_info:
            info["license"] = self.license_info

        return {
            "openapi": "3.0.2",
            "info": info,
            "paths": self._generate_paths(),
            "components": {"schemas": self.schemas},
            "tags": self._generate_tags(),
        }

    def _generate_tags(self) -> List[Dict[str, str]]:
        """Génère la liste des tags utilisés"""
        tags_set = set()
        for route in self.routes:
            tags_set.update(route.tags)

        return [
            {"name": tag, "description": f"Opérations liées à {tag}"} for tag in sorted(tags_set)
        ]

    def _generate_paths(self) -> Dict[str, Any]:
        """Génère la section 'paths' de l'OpenAPI"""
        paths: Dict[str, Any] = {}

        for route in self.routes:
            if not route.include_in_schema:
                continue

            openapi_path = self._convert_path_to_openapi(route.path)

            if openapi_path not in paths:
                paths[openapi_path] = {}

            for method in route.methods:
                paths[openapi_path][method.lower()] = self._generate_operation(route, openapi_path)

        return paths

    def _convert_path_to_openapi(self, path: str) -> str:
        """
        Convertit un chemin Starlette en chemin OpenAPI
        /todos/{todo_id} -> /todos/{todo_id} (déjà compatible)
        """
        return path

    def _generate_operation(self, route: RouteInfo, path: str) -> Dict[str, Any]:
        """Génère une opération OpenAPI pour une route avec documentation complète"""
        sig = inspect.signature(route.func)
        parameters = []
        request_body = None

        # Extraire les paramètres de chemin depuis le path
        path_params = re.findall(r"\{(\w+)\}", path)

        # Extraire la docstring pour enrichir la documentation
        docstring = self._parse_docstring(route.func)

        for param_name, param in sig.parameters.items():
            # Ignorer les paramètres spéciaux
            if param_name in ["self", "cls", "request", "db"]:
                continue

            # Ignorer les paramètres avec Depends()
            if param.default != inspect.Parameter.empty:
                if (
                    hasattr(param.default, "__class__")
                    and param.default.__class__.__name__ == "Depends"
                ):
                    continue

            annotation = param.annotation

            # Vérifier si c'est un modèle Pydantic
            if self._is_pydantic_model(annotation):
                # C'est un body
                schema = annotation.model_json_schema()

                # Ajouter le schéma aux components pour réutilisation
                schema_name = annotation.__name__
                self.schemas[schema_name] = schema

                request_body = {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{schema_name}"},
                            "example": self._generate_example(annotation),
                        }
                    },
                    "description": f"Données {schema_name} à envoyer",
                }
            else:
                # Déterminer le type et format
                param_info = self._get_parameter_info(annotation, param)

                # Déterminer si c'est un path param ou query param
                param_in = "path" if param_name in path_params else "query"

                # Description du paramètre depuis la docstring
                param_description = docstring.get("params", {}).get(param_name, "")

                param_schema = {
                    "name": param_name,
                    "in": param_in,
                    "required": param_in == "path" or param.default == inspect.Parameter.empty,
                    "schema": param_info["schema"],
                    "description": param_description or f"Paramètre {param_name}",
                }

                # Ajouter des exemples si disponibles
                if "example" in param_info:
                    param_schema["example"] = param_info["example"]

                # Ajouter valeur par défaut si présente
                if param.default != inspect.Parameter.empty:
                    param_schema["schema"]["default"] = param.default

                parameters.append(param_schema)

        # Construction de l'opération
        operation = {
            "summary": route.summary or docstring.get("summary", f"{route.methods[0]} {path}"),
            "description": route.description or docstring.get("description", ""),
            "tags": route.tags or ["default"],
            "operationId": self._generate_operation_id(route, path),
            "parameters": parameters,
            "responses": self._generate_responses(route, docstring),
        }

        if request_body:
            operation["requestBody"] = request_body

        if route.deprecated:
            operation["deprecated"] = True

        return operation

    def _generate_operation_id(self, route: RouteInfo, path: str) -> str:
        """Génère un ID unique pour l'opération"""
        method = route.methods[0].lower()
        [p for p in path.split("/") if p and not p.startswith("{")]
        func_name = route.func.__name__
        return f"{method}_{func_name}"

    def _parse_docstring(self, func: callable) -> Dict[str, Any]:
        """Parse la docstring pour extraire summary, description et params"""
        doc = inspect.getdoc(func)
        if not doc:
            return {}

        lines = doc.split("\n")
        result = {"summary": "", "description": "", "params": {}, "returns": "", "raises": []}

        current_section = None
        summary_lines = []
        description_lines = []

        for line in lines:
            line = line.strip()

            if not line:
                continue

            # Détecter les sections
            if line.lower().startswith("args:") or line.lower().startswith("parameters:"):
                current_section = "params"
                continue
            elif line.lower().startswith("returns:"):
                current_section = "returns"
                continue
            elif line.lower().startswith("raises:"):
                current_section = "raises"
                continue

            # Parser selon la section
            if current_section == "params":
                # Format: param_name: description
                if ":" in line:
                    param_match = re.match(r"(\w+):\s*(.+)", line)
                    if param_match:
                        param_name, param_desc = param_match.groups()
                        result["params"][param_name] = param_desc
            elif current_section == "returns":
                result["returns"] += line + " "
            elif current_section == "raises":
                result["raises"].append(line)
            else:
                # Partie avant les sections = summary + description
                if not summary_lines:
                    summary_lines.append(line)
                else:
                    description_lines.append(line)

        result["summary"] = " ".join(summary_lines)
        result["description"] = " ".join(description_lines)

        return result

    def _generate_responses(self, route: RouteInfo, docstring: Dict) -> Dict[str, Any]:
        """Génère les réponses possibles avec descriptions enrichies"""
        responses = {
            str(route.status_code): {
                "description": docstring.get("returns", "Opération réussie"),
                "content": {
                    "application/json": {"schema": self._get_response_schema(route.response_model)}
                },
            }
        }

        # Ajouter les erreurs depuis la docstring
        if docstring.get("raises"):
            for error in docstring["raises"]:
                if "NotFoundException" in error or "404" in error:
                    responses["404"] = {
                        "description": error,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "error": {"type": "string"},
                                        "details": {"type": "string"},
                                    },
                                },
                                "example": {
                                    "error": "Ressource non trouvée",
                                    "details": "L'élément demandé n'existe pas",
                                },
                            }
                        },
                    }

        # Erreurs standards
        responses["422"] = {
            "description": "Erreur de validation des données",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "error": {"type": "string"},
                            "details": {"type": "array", "items": {"type": "object"}},
                        },
                    },
                    "example": {
                        "error": "Validation error",
                        "details": [
                            {
                                "loc": ["body", "field_name"],
                                "msg": "field required",
                                "type": "value_error.missing",
                            }
                        ],
                    },
                }
            },
        }

        responses["500"] = {
            "description": "Erreur interne du serveur",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {"error": {"type": "string"}, "type": {"type": "string"}},
                    }
                }
            },
        }

        return responses

    def _get_response_schema(self, response_model: Any) -> Dict[str, Any]:
        """Génère le schéma de réponse"""
        if not response_model:
            return {"type": "object"}

        if self._is_pydantic_model(response_model):
            schema_name = response_model.__name__
            self.schemas[schema_name] = response_model.model_json_schema()
            return {"$ref": f"#/components/schemas/{schema_name}"}

        return {"type": "object"}

    def _get_parameter_info(self, annotation: Any, param: inspect.Parameter) -> Dict[str, Any]:
        """Extrait les informations détaillées d'un paramètre"""
        result = {"schema": {"type": "string"}, "example": None}

        # Types de base
        type_mapping = {
            int: ("integer", "int32", 42),
            float: ("number", "float", 3.14),
            str: ("string", None, "example"),
            bool: ("boolean", None, True),
        }

        if annotation in type_mapping:
            type_name, format_name, example = type_mapping[annotation]
            result["schema"]["type"] = type_name
            if format_name:
                result["schema"]["format"] = format_name
            result["example"] = example

        # Types optionnels (Optional[T])
        origin = get_origin(annotation)
        if origin is not None:
            args = get_args(annotation)

            # Optional[X] = Union[X, None]
            if len(args) == 2 and type(None) in args:
                inner_type = args[0] if args[1] is type(None) else args[1]
                result = self._get_parameter_info(inner_type, param)
                result["schema"]["nullable"] = True

            # List[X]
            elif origin == list:
                result["schema"] = {
                    "type": "array",
                    "items": self._get_parameter_info(args[0], param)["schema"],
                }

        return result

    def _generate_example(self, model) -> Optional[Dict]:
        """Génère un exemple depuis un modèle Pydantic"""
        if not self._is_pydantic_model(model):
            return None

        try:
            # Utiliser model_json_schema pour extraire les exemples
            schema = model.model_json_schema()
            if "example" in schema:
                return schema["example"]

            # Générer un exemple basique
            example = {}
            if "properties" in schema:
                for field_name, field_schema in schema["properties"].items():
                    field_type = field_schema.get("type", "string")

                    if field_type == "string":
                        example[field_name] = f"example_{field_name}"
                    elif field_type == "integer":
                        example[field_name] = 1
                    elif field_type == "number":
                        example[field_name] = 1.0
                    elif field_type == "boolean":
                        example[field_name] = True
                    elif field_type == "array":
                        example[field_name] = []
                    else:
                        example[field_name] = {}

            return example
        except:
            return None

    def _is_pydantic_model(self, annotation) -> bool:
        """Vérifie si une annotation est un modèle Pydantic"""
        try:
            return hasattr(annotation, "model_json_schema")
        except:
            return False

    def _get_type_from_annotation(self, annotation) -> str:
        """Convertit une annotation Python en type OpenAPI"""
        type_mapping = {
            int: "integer",
            float: "number",
            str: "string",
            bool: "boolean",
            list: "array",
            dict: "object",
        }

        return type_mapping.get(annotation, "string")
