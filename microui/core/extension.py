"""
Système de composants HTML en classes Python
Permet de créer des composants réutilisables avec props et composition
"""
from typing import Optional, List, Dict, Any
from markupsafe import Markup # type: ignore
from abc import ABC, abstractmethod


class Component(ABC):
    """Classe de base pour tous les composants"""
    
    def __init__(self, **props):
        self.props = props
        self.children = []
    
    def add_child(self, child):
        """Ajoute un enfant au composant"""
        if isinstance(child, (Component, str)):
            self.children.append(child)
        return self
    
    def __call__(self, *children):
        """Permet d'ajouter des enfants avec la syntaxe: Component()(child1, child2)"""
        for child in children:
            self.add_child(child)
        return self
    
    @abstractmethod
    def render(self) -> str:
        """Méthode abstraite que chaque composant doit implémenter"""
        pass
    
    def __str__(self):
        return self.render()
    
    def __html__(self):
        return Markup(self.render())
    
    def _render_children(self) -> str:
        """Rend tous les enfants du composant"""
        return "".join(
            child.render() if isinstance(child, Component) else str(child)
            for child in self.children
        )