# Étude de cas — Gestion des rendez-vous d’un cabinet médical

**Cours :** Technologies Web 2.0 · **Année universitaire :** 2026–2027  
**Source :** `case_study.docx` (2 pages). Ce document reprend les exigences de l'énoncé ; il ne décrit pas encore une implémentation terminée.

## 1. Objectif

Développer une application web de gestion des rendez-vous d’un cabinet médical avec :

- un **Front-Office** ;
- un **Back-Office** ;
- une **API REST** via **Django REST Framework**.

## 2. Modèle métier

L’application comporte quatre entités métier : **Medecin**, **Patient**, **Specialite** et **RendezVous**, ainsi qu’un modèle **User** hérité de `AbstractUser`.

### Héritage

- `User` hérite de `AbstractUser`.
- `Medecin` et `Patient` héritent de `User` par **héritage multi-tables**.
- `username`, `password`, `email`, `first_name` et `last_name` sont hérités ; **ne pas les redéclarer**.

### Entités et attributs du diagramme d'analyse

| Entité | Champs indiqués dans le diagramme |
|---|---|
| `User` | `id`, `username`, `password`, `email`, `first_name`, `last_name` (via `AbstractUser`) |
| `Medecin` | `matricule_ordre` (chaîne, clé primaire, longueur 6), `telephone` (chaîne, 8 chiffres) |
| `Patient` | `cin` (chaîne, clé primaire, 8 chiffres), `telephone` (chaîne, 8 chiffres), `date_naissance` (date, au plus tard aujourd'hui) |
| `Specialite` | `id` (entier), `nom_specialite` (chaîne) |
| `RendezVous` | `id` (entier), `motif` (texte), `ordonnance` (fichier PDF facultatif), `statut` (`EN_ATTENTE` par défaut), `duree_minutes` (entier, 30 par défaut), `date_rdv` (date/heure future), `date_creation` (date/heure), `date_maj` (date/heure) |

**Statuts présentés dans le diagramme :** `EN_ATTENTE`, `CONFIRME`, `ANNULE`.

> Les attributs ci-dessus sont retranscrits à partir du diagramme de classes en page 1. Vérifier leur orthographe et les contraintes exactes contre le document original avant de coder les modèles.

### Associations et cardinalités

| Source | Cible | Multiplicité | Champ / rôle |
|---|---|---|---|
| `RendezVous` | `Medecin` | plusieurs → un | `medecin` (praticien) |
| `RendezVous` | `Patient` | plusieurs → un | `patient` (demandeur) |
| `Medecin` | `Specialite` | plusieurs ↔ plusieurs | `specialites` (`ManyToManyField` simple) |

**Contraintes de modélisation :**

- `RendezVous` est une entité autonome avec son propre identifiant et deux `ForeignKey` simples vers `Medecin` et `Patient`.
- Un même couple médecin–patient peut avoir **plusieurs rendez-vous**.
- Ne **pas** représenter les rendez-vous par un `ManyToManyField` ou une classe `through`.
- La seule relation `ManyToManyField` demandée relie `Medecin` et `Specialite`, sans `through` personnalisé.

## 3. Mise en place demandée dans l'énoncé

- **Django :** version **5.2 LTS**.
- **Python :** version **3.12**.
- **Environnement virtuel :** `env`.
- **Nom du projet Django :** `GestionCabinetMedical`.
- **Applications Django :**
  - `Cabinet` : `User`, `Specialite`, `Medecin`, `Patient` ;
  - `RendezVous` : `RendezVous`.

## 4. État local connu (distinct des exigences)

L'installation déjà réalisée dans le répertoire `MyProject/` utilise :

| Élément | Exigence du sujet | État local constaté |
|---|---|---|
| Python | 3.12 | 3.14.10 |
| Django | 5.2 LTS | 5.2.19 |
| Environnement | `env` | `.venv` géré par `uv` |
| Projet Django | `GestionCabinetMedical` | `config` |
| Dossier racine | non précisé | `MyProject` |
| Applications | `Cabinet`, `RendezVous` | pas encore créées dans les sorties fournies |
| Base de données | non précisée | SQLite (`db.sqlite3`) |

**À décider avant de modifier la structure :** faut-il reproduire *exactement* les noms et Python 3.12 demandés pour la remise, ou l'enseignant accepte-t-il une installation équivalente avec `uv` et Python 3.14 ? Le document ne précise pas si ces substitutions sont autorisées.

## 5. Prochaines étapes proposées (plan, pas exigences supplémentaires)

1. Conserver le document source et ce fichier Markdown dans le dépôt.
2. Aligner prudemment le nom du projet et les applications avec l'énoncé.
3. Configurer le modèle utilisateur personnalisé **avant** de créer les migrations métier ; ce choix est sensible dans Django.
4. Implémenter les modèles et leurs relations, puis les migrations.
5. Développer progressivement le Back-Office, le Front-Office et l'API REST.

> **Périmètre :** seules les deux pages fournies ont été documentées. Aucun parcours utilisateur ni endpoint API précis n'est spécifié dans ces pages.
