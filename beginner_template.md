# Architecture Template Minimale SolidKnowledge
## Pour Débutants DDD et Programmation

---

## 🎯 Vision Globale

Cette architecture est une **graine initiale** qui contient tout le nécessaire pour démarrer sans jamais bloquer un agent IA ou un développeur débutant. Elle suit les principes SolidKnowledge : **aspirer, déconstruire, composer**.

### Principe Fondamental : Le Trio Atomique

```
Chaque module = 3 fichiers (jamais moins)
├─ intention.md      # POURQUOI (langage naturel)
├─ implementation.*  # COMMENT (code)
└─ validation.test.* # PREUVE (tests)
```

**Source** : Document "Modélisation Formelle - Stratégie de tests et architecture fractale"
> "Architecture Fractale : Le Trio Atomique [...] Un Atome est l'unité minimale de cohésion fonctionnelle."

---

## 📁 Structure Arborescente Minimale

```
mon_projet/
├─ README.md                        # Point d'entrée humain
├─ meta_domain/                     # Graphe de pensée (avant le code)
│  ├─ notes_concepts/              # Notes #domain
│  ├─ notes_strategies/            # Notes #application  
│  └─ event_storming/              # Événements découverts
│
└─ src/
   ├─ domain/                      # CŒUR STABLE - Logique métier pure
   │  ├─ _base/
   │  │  ├─ intention.md
   │  │  ├─ entity.py             # Classe de base Entity
   │  │  ├─ entity.test.py
   │  │  ├─ value_object.py       # Classe de base ValueObject
   │  │  ├─ value_object.test.py
   │  │  ├─ aggregate_root.py     # Classe de base Aggregate
   │  │  ├─ aggregate_root.test.py
   │  │  ├─ domain_event.py       # Classe de base Event
   │  │  └─ domain_event.test.py
   │  │
   │  ├─ entities/                # Vos objets métier avec identité
   │  │  └─ .gitkeep
   │  │
   │  ├─ value_objects/           # Vos concepts sans identité
   │  │  └─ .gitkeep
   │  │
   │  ├─ aggregates/              # Racines de cohérence transactionnelle
   │  │  └─ .gitkeep
   │  │
   │  ├─ events/                  # Événements du domaine
   │  │  └─ .gitkeep
   │  │
   │  └─ repositories/            # INTERFACES seulement (contrats)
   │     ├─ intention.md
   │     ├─ i_repository.py       # Interface générique
   │     └─ i_repository.test.py
   │
   ├─ application/                # SEMI-STABLE - Orchestration
   │  ├─ _base/
   │  │  ├─ intention.md
   │  │  ├─ command.py            # Base Command
   │  │  ├─ query.py              # Base Query
   │  │  └─ use_case.py           # Template UseCase
   │  │
   │  ├─ commands/
   │  │  ├─ intention.md
   │  │  ├─ command_bus.py
   │  │  ├─ command_bus.test.py
   │  │  ├─ handler_registry.py
   │  │  └─ handler_registry.test.py
   │  │
   │  ├─ queries/
   │  │  ├─ intention.md
   │  │  ├─ query_bus.py
   │  │  ├─ query_bus.test.py
   │  │  ├─ handler_registry.py
   │  │  └─ handler_registry.test.py
   │  │
   │  └─ services/               # Vos cas d'usage (Use Cases)
   │     └─ exemple_service/
   │        ├─ intention.md
   │        ├─ i_api_exemple_service.py  # Interface API
   │        ├─ dtos/
   │        │  ├─ exemple_request_dto.py
   │        │  └─ exemple_response_dto.py
   │        ├─ exemple_service.py
   │        └─ exemple_service.test.py
   │
   └─ infrastructure/             # VOLATILE - Détails techniques
      ├─ _common/
      │  ├─ serialization/
      │  │  ├─ intention.md
      │  │  ├─ serializer.py
      │  │  ├─ serializer.test.py
      │  │  ├─ event_serializer.py
      │  │  └─ event_serializer.test.py
      │  │
      │  ├─ validation/
      │  │  ├─ intention.md
      │  │  ├─ invariant_validator.py
      │  │  └─ invariant_validator.test.py
      │  │
      │  └─ transactions/
      │     ├─ intention.md
      │     ├─ unit_of_work.py
      │     └─ unit_of_work.test.py
      │
      ├─ events/
      │  ├─ bus/
      │  │  ├─ intention.md
      │  │  ├─ event_bus.py
      │  │  ├─ event_bus.test.py
      │  │  └─ fake/
      │  │     ├─ intention.md
      │  │     ├─ in_memory_bus.py
      │  │     └─ in_memory_bus.test.py
      │  │
      │  └─ store/
      │     ├─ intention.md
      │     ├─ event_store.py        # Capteur universel
      │     ├─ event_store.test.py
      │     ├─ stored_event.py
      │     └─ fake/
      │        ├─ intention.md
      │        ├─ in_memory_event_store.py
      │        └─ in_memory_event_store.test.py
      │
      ├─ persistence/
      │  └─ repositories/
      │     └─ fake/
      │        ├─ intention.md
      │        ├─ in_memory_repository.py  # Générique
      │        └─ in_memory_repository.test.py
      │
      └─ observability/
         ├─ logging/
         │  ├─ intention.md
         │  ├─ structured_logger.py
         │  └─ structured_logger.test.py
         │
         └─ metrics/
            ├─ intention.md
            ├─ metrics_collector.py
            ├─ metrics_collector.test.py
            ├─ event_store_metrics.py
            └─ event_store_metrics.test.py
```

---

## 🧬 Principes DDD Appliqués (avec Sources)

### 1. Aggregate Root - Le Gardien de Cohérence

**Définition DDD** :
> "Choose one ENTITY to be the 'root' of each AGGREGATE, and control all access to the objects inside the boundary through the root."
> — **Source** : Implementing Domain-Driven Design (Vernon), Chapter 10 "Aggregates"

**Votre Document** :
> "∀ FA : ∃! Aggregate A tel que FA modifie exactement un Aggregate"
> — **Source** : "Concept Fonctionnalité Atomique SolidAI - Définition"

**Exemple pour Débutant** :
```python
# domain/aggregates/commande/commande.py

class Commande(AggregateRoot):
    """
    AGGREGATE ROOT = Point d'entrée unique pour modifier l'état
    
    Règle : Toutes les modifications passent par cette classe
    Les lignes de commande ne peuvent être modifiées que via Commande
    """
    
    def __init__(self, commande_id: CommandeId):
        super().__init__(commande_id)
        self._lignes = []  # Entités internes protégées
        self._statut = StatutCommande.BROUILLON
    
    def ajouter_ligne(self, produit: ProduitId, quantite: Quantite):
        """Logique métier : on ne peut ajouter que si BROUILLON"""
        if self._statut != StatutCommande.BROUILLON:
            raise CommandeNonModifiable()
        
        ligne = LigneCommande(produit, quantite)
        self._lignes.append(ligne)
        
        # Émet un événement
        self.record_event(LigneAjoutee(self.id, produit, quantite))
```

---

### 2. Value Object - L'Immuabilité Conceptuelle

**Définition DDD** :
> "When you care only about the attributes and logic of an element of the model, classify it as a VALUE OBJECT. Make it express the meaning of the attributes it conveys and give it related functionality. Treat the VALUE OBJECT as immutable."
> — **Source** : Implementing Domain-Driven Design (Vernon), Chapter 6 "Value Objects"

**Exemple pour Débutant** :
```python
# domain/value_objects/quantite/quantite.py

from dataclasses import dataclass

@dataclass(frozen=True)  # frozen = immuable
class Quantite:
    """
    VALUE OBJECT = Valeur sans identité
    
    Deux quantités sont égales si elles ont la même valeur
    On ne peut pas "modifier" une quantité, on en crée une nouvelle
    """
    
    valeur: int
    
    def __post_init__(self):
        # Invariant métier
        if self.valeur <= 0:
            raise QuantiteInvalide(f"Quantité doit être > 0, reçu {self.valeur}")
    
    def ajouter(self, autre: 'Quantite') -> 'Quantite':
        """Retourne une NOUVELLE quantité (immuable)"""
        return Quantite(self.valeur + autre.valeur)
```

---

### 3. Repository - L'Abstraction de Persistance

**Définition DDD** :
> "A REPOSITORY represents all objects of a certain type as a conceptual set [...] Methods for adding and removing objects, which will encapsulate the actual insertion or removal of data in the data store."
> — **Source** : Implementing Domain-Driven Design (Vernon), Chapter 12 "Repositories"

**Votre Document** :
> "Repository Interface ∈ Domain (abstraction stable). Implémentations possibles : PostgresRepository ∈ Infrastructure/Real, InMemoryRepository ∈ Infrastructure/Fake"
> — **Source** : "Modélisation Formelle - Stratégie de tests et architecture fractale"

**Exemple pour Débutant** :
```python
# domain/repositories/i_commande_repository.py

from abc import ABC, abstractmethod

class ICommandeRepository(ABC):
    """
    INTERFACE (contrat) dans Domain
    = Ce que le domaine attend, pas comment c'est fait
    """
    
    @abstractmethod
    def trouver_par_id(self, commande_id: CommandeId) -> Optional[Commande]:
        """Chercher une commande"""
        pass
    
    @abstractmethod
    def sauvegarder(self, commande: Commande) -> None:
        """Persister les changements"""
        pass

# infrastructure/persistence/repositories/fake/in_memory_commande_repository.py

class InMemoryCommandeRepository(ICommandeRepository):
    """
    IMPLÉMENTATION Fake pour tests/développement
    Stocke en mémoire (dict Python)
    """
    
    def __init__(self):
        self._commandes: Dict[CommandeId, Commande] = {}
    
    def trouver_par_id(self, commande_id: CommandeId) -> Optional[Commande]:
        return self._commandes.get(commande_id)
    
    def sauvegarder(self, commande: Commande) -> None:
        self._commandes[commande.id] = commande
```

---

### 4. Application Service - L'Orchestrateur Sans Logique Métier

**Définition DDD** :
> "Application Services reside in the Application Layer. These are different from Domain Services and are thus devoid of domain logic. They may control persistence transactions and security."
> — **Source** : Implementing Domain-Driven Design (Vernon), Chapter 14 "Application"

**Votre Document** :
> "API Application : Ensemble des opérations publiques exposées par la couche Application [...] Service : Implémentation concrète orchestrant la logique applicative."
> — **Source** : "API Interface et Implémentation"

**Exemple pour Débutant** :
```python
# application/services/creer_commande_service/creer_commande_service.py

class CreerCommandeService:
    """
    APPLICATION SERVICE = Chef d'orchestre
    
    Responsabilités :
    - Charger les données (via Repository)
    - Appeler la logique domaine (Aggregate)
    - Sauvegarder (via Repository)
    - Publier événements (via EventBus)
    
    PAS de logique métier ici !
    """
    
    def __init__(
        self, 
        repository: ICommandeRepository,
        event_bus: IEventBus
    ):
        self._repository = repository
        self._event_bus = event_bus
    
    def executer(self, request: CreerCommandeRequest) -> CreerCommandeResponse:
        # 1. Créer l'objet domaine (logique = dans l'Aggregate)
        commande = Commande(CommandeId.generer())
        
        # 2. Sauvegarder
        self._repository.sauvegarder(commande)
        
        # 3. Publier événements
        for event in commande.events:
            self._event_bus.publish(event)
        
        # 4. Retourner résultat
        return CreerCommandeResponse(commande_id=commande.id)
```

---

### 5. Domain Event - La Mémoire du Système

**Définition DDD** :
> "Model information about activity in the domain as a series of discrete events. Represent each event as a domain object [...] A domain event is a full-fledged part of the domain model."
> — **Source** : Implementing Domain-Driven Design (Vernon), Chapter 8 "Domain Events"

**Votre Document** :
> "EventStore = Capteur Universel du Système [...] TOUS les DomainEvents y sont persistés"
> — **Source** : "Initiation Projet - EventStore vu comme un capteur universel"

**Exemple pour Débutant** :
```python
# domain/events/ligne_ajoutee.py

from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class LigneAjoutee(DomainEvent):
    """
    DOMAIN EVENT = Quelque chose s'est passé
    
    - Nommé au passé (LigneAjoutée, pas AjouterLigne)
    - Immuable (ce qui s'est passé ne change pas)
    - Contient toutes les infos nécessaires
    """
    
    commande_id: CommandeId
    produit_id: ProduitId
    quantite: Quantite
    timestamp: datetime
    
    @property
    def event_type(self) -> str:
        return "commande.ligne_ajoutee"
```

---

## 🎓 Guide d'Utilisation pour Débutant

### Étape 1 : Comprendre le Meta-Domain (Avant le Code)

**Principe SolidKnowledge** :
> "Intention floue (user) → Notes Concepts (#domain) → Notes Stratégies (#application) → Notes Implémentation (#infra)"
> — **Source** : "Concept - Modélisation Intention Utilisateur - Graphe de la pensée"

**Exercice pratique** :
```markdown
meta_domain/event_storming/session_01.md

# Event Storming - Système de Commandes

## Événements Découverts (orange)
- CommandeCreee
- LigneAjoutee
- CommandeValidee
- CommandeAnnulee

## Commandes (bleu)
- CreerCommande
- AjouterLigne
- ValiderCommande

## Aggregates (jaune)
- Commande (racine)

## Règles Métier (rose)
- On ne peut ajouter des lignes que si BROUILLON
- Une commande validée ne peut plus être modifiée
```

---

### Étape 2 : Créer Votre Premier Aggregate

**Template intention.md** :
```markdown
# Aggregate Commande

## Rationale
- Global context: Gestion du cycle de vie des commandes clients
- Why adapted here: Garantir cohérence transactionnelle (commande + lignes)

## Responsibility
Garantir qu'une commande respecte les règles métier à chaque modification

## Design
Aggregate Root avec événements
- Pattern : Command + Event Sourcing
- Invariants : Statut cohérent, lignes valides
```

**Code minimal** :
```python
# domain/aggregates/commande/commande.py

class Commande(AggregateRoot):
    def __init__(self, commande_id: CommandeId):
        super().__init__(commande_id)
        self._statut = StatutCommande.BROUILLON
        self._lignes = []
    
    # Logique métier pure
    def valider(self):
        if len(self._lignes) == 0:
            raise CommandeVide()
        
        self._statut = StatutCommande.VALIDEE
        self.record_event(CommandeValidee(self.id))
```

**Test** :
```python
# domain/aggregates/commande/commande.test.py

def test_commande_vide_ne_peut_etre_validee():
    # Given
    commande = Commande(CommandeId.generer())
    
    # When / Then
    with pytest.raises(CommandeVide):
        commande.valider()
```

---

### Étape 3 : Créer Votre Premier Use Case

**Structure minimale** :
```python
# application/services/valider_commande_service/valider_commande_service.py

class ValiderCommandeService:
    def __init__(self, repository: ICommandeRepository):
        self._repository = repository
    
    def executer(self, request: ValiderCommandeRequest):
        # 1. Charger
        commande = self._repository.trouver_par_id(request.commande_id)
        
        # 2. Appeler domaine
        commande.valider()  # Logique = dans l'Aggregate
        
        # 3. Sauvegarder
        self._repository.sauvegarder(commande)
        
        return ValiderCommandeResponse(success=True)
```

**Test avec Fake** :
```python
# application/services/valider_commande_service/valider_commande_service.test.py

def test_valider_commande_success():
    # Given
    repository = InMemoryCommandeRepository()  # Fake
    service = ValiderCommandeService(repository)
    
    commande = Commande(CommandeId("cmd-123"))
    commande.ajouter_ligne(ProduitId("prod-1"), Quantite(2))
    repository.sauvegarder(commande)
    
    # When
    result = service.executer(ValiderCommandeRequest("cmd-123"))
    
    # Then
    assert result.success == True
    commande_saved = repository.trouver_par_id(CommandeId("cmd-123"))
    assert commande_saved.statut == StatutCommande.VALIDEE
```

---

## 📊 Règles de Dépendance (Dependency Rule)

**Source DDD** :
> "The inner layers define interfaces. The outer layers implement those interfaces. The direction of dependency is inward."
> — **Source** : Implementing Domain-Driven Design (Vernon), Architecture Hexagonale

**Votre Formalisation** :
```
Adapters → Application → Domain
Infrastructure → Domain (via interfaces)

∀ couche C₁, C₂ : 
    niveau(C₁) > niveau(C₂) ⟹ C₁ dépend de C₂
    niveau(C₁) < niveau(C₂) ⟹ C₁ ⊥ C₂
```
> — **Source** : "Concept Fonctionnalité Atomique SolidAI - Définition"

**Règles Simples** :
1. ✅ **Application peut importer Domain**
2. ✅ **Infrastructure peut importer Domain (interfaces)**
3. ❌ **Domain NE PEUT JAMAIS importer Infrastructure**
4. ❌ **Domain NE PEUT JAMAIS importer Application**

**Exemple d'erreur** :
```python
# ❌ INTERDIT dans domain/aggregates/commande.py
from infrastructure.persistence import PostgresRepository  # NON !

# ✅ CORRECT
from domain.repositories import ICommandeRepository  # Interface seulement
```

---

## 🧪 Stratégie de Tests (Pyramide)

**Votre Formalisation** :
```
Tests Domain → validé avec objets purs
Tests Application → validé avec Fakes
Fake validé → garantit le contrat
Real implémenté → respecte le contrat
```
> — **Source** : "Modélisation Formelle - Stratégie de tests et architecture fractale"

**Distribution Cible** :
- **70%** Tests Domain (rapides, < 10ms)
- **20%** Tests Application avec Fakes
- **10%** Tests Infrastructure Real (lents, I/O)

**Exemple complet** :
```python
# 1. Test Domain (pur)
def test_commande_invariant_lignes_positives():
    commande = Commande(CommandeId("cmd-1"))
    
    with pytest.raises(QuantiteInvalide):
        commande.ajouter_ligne(ProduitId("p1"), Quantite(-5))

# 2. Test Application (avec Fake)
def test_use_case_avec_fake():
    fake_repo = InMemoryCommandeRepository()
    service = ValiderCommandeService(fake_repo)
    # ... test complet

# 3. Test Infrastructure Real (intégration)
def test_postgres_repository():
    real_repo = PostgresCommandeRepository(db_connection)
    # ... test avec vraie DB
```

---

## 🎯 Métriques de Cohérence SolidAI

**Votre Système de Métriques** :
```yaml
Métriques de Cohésion :
├─ Cohésion par Atome : [0, 1]
├─ Sync Meta-Domain/Code : [0, 1]
├─ Complétude Trio (intention + code + test) : {0, 1}
└─ Distance sémantique : ℝ⁺
```
> — **Source** : "Modélisation Formelle - Stratégie de tests et architecture fractale"

**Pour Débutant - Checklist Manuelle** :
- [ ] Chaque dossier a son `intention.md` ?
- [ ] Chaque `.py` a son `.test.py` ?
- [ ] Les tests passent tous ?
- [ ] Domain n'importe rien d'Infrastructure ?
- [ ] Tous les Aggregates ont des événements ?
- [ ] EventStore capture tous les événements ?

---

## 🚀 Premier Projet : TODO List en DDD

### Event Storming
```
Événements : TacheCreee, TacheCompletee, TacheArchivee
Commandes : CreerTache, CompleterTache, ArchiverTache
Aggregate : Tache
```

### Structure Minimale
```
src/
├─ domain/
│  ├─ aggregates/tache/
│  │  ├─ intention.md
│  │  ├─ tache.py
│  │  └─ tache.test.py
│  ├─ value_objects/description/
│  │  ├─ intention.md
│  │  ├─ description.py
│  │  └─ description.test.py
│  └─ events/
│     ├─ tache_creee.py
│     └─ tache_completee.py
│
├─ application/services/
│  └─ creer_tache_service/
│     ├─ intention.md
│     ├─ i_api_creer_tache_service.py
│     ├─ dtos/
│     │  ├─ creer_tache_request_dto.py
│     │  └─ creer_tache_response_dto.py
│     ├─ creer_tache_service.py
│     └─ creer_tache_service.test.py
│
└─ infrastructure/
   ├─ events/store/
   │  ├─ fake/in_memory_event_store.py
   │  └─ fake/in_memory_event_store.test.py
   └─ persistence/repositories/
      └─ fake/in_memory_tache_repository.py
```

---

## 📚 Sources et Lectures Complémentaires

### Sources Citées

1. **Implementing Domain-Driven Design** (Vaughn Vernon)
   - Chapter 6: Value Objects
   - Chapter 8: Domain Events
   - Chapter 10: Aggregates
   - Chapter 12: Repositories
   - Chapter 14: Application Services

2. **Documents SolidKnowledge**
   - "Concept Fonctionnalité Atomique SolidAI - Définition"
   - "Modélisation Formelle - Stratégie de tests et architecture fractale"
   - "Initiation Projet - EventStore vu comme un capteur universel"
   - "API Interface et Implémentation"
   - "SolidAI - Graine Initiale - Dtos"

### Principes Clés à Retenir

1. **Fractalité** : Trio atomique à tous les niveaux
2. **Stabilité** : Domain stable, Infrastructure volatile
3. **Observation** : EventStore capture tout
4. **Navigation** : O(1) grâce à co-localisation
5. **Testabilité** : Fakes permettent tests rapides

---

## ✅ Checklist de Démarrage

### Jour 1 : Setup Initial
- [ ] Créer l'arborescence minimale
- [ ] Copier les classes de base (_base/)
- [ ] Configurer EventStore + Fake

### Jour 2 : Premier Aggregate
- [ ] Event Storming papier
- [ ] Créer 1 Aggregate avec intention.md
- [ ] Écrire 3 tests Domain

### Jour 3 : Premier Use Case
- [ ] Créer Application Service
- [ ] Écrire tests avec Fake Repository
- [ ] Vérifier EventStore capture événements

### Jour 4 : Métriques
- [ ] Compter tests rapides vs lents
- [ ] Vérifier complétude Trio atomique
- [ ] Observer événements dans EventStore

---

## 🎓 Aide-Mémoire pour Débutant

**Quand créer un Aggregate ?**
→ Quand il y a une règle métier qui relie plusieurs concepts

**Quand créer un Value Object ?**
→ Quand c'est une valeur mesurable/comparable sans identité

**Quand créer un Domain Event ?**
→ Quand quelque chose d'important s'est passé métier

**Où mettre la logique métier ?**
→ TOUJOURS dans Domain (Aggregate/Entity/ValueObject)

**C'est quoi un Fake ?**
→ Une vraie implémentation simplifiée (en mémoire) pour tests rapides

**Pourquoi intention.md ?**
→ Pont entre votre cerveau et le code, synchronisation humain/machine

---

**Cette architecture est votre graine. Faites-la croître, événement par événement.**