# xml2xml

`xml2xml` est un script Python permettant de traduire automatiquement des fichiers XML, en ciblant certains tags définis par type de question. Il utilise le module `lxml` pour manipuler les fichiers XML et `translate` de Google Cloud pour la traduction.

---

## Installation

1. Cloner le dépôt :

```bash
git clone <URL_DU_DEPOT>
cd <REPERTOIRE_DU_DEPOT>
```

2. Installer les dépendances Python (idéalement dans un environnement virtuel) :

```bash
pip install lxml google-cloud-translate
```

> ⚠️ Il est nécessaire de configurer un compte Google Cloud pour utiliser le module `translate`.
> Vous pouvez remplacer la fonction de traduction par une autre si vous le souhaitez.

---

## Utilisation

### Traduire un ensemble de fichiers

Par défaut, les fichiers traduits sont générés dans le répertoire courant. Pour traduire plusieurs fichiers XML :

```bash
python3 bin/xml2xml.py -i examples/*.xml
```

Exemple de sortie :

```
examples/coderunner.xml -> ./coderunner_en.xml
examples/matching.xml -> ./matching_en.xml
examples/multichoice.xml -> ./multichoice_en.xml
examples/numerical.xml -> ./numerical_en.xml
examples/shortanswer.xml -> ./shortanswer_en.xml
```

### Définir un répertoire de sortie

Vous pouvez préciser un répertoire de sortie avec l'option `-o` :

```bash
python3 bin/xml2xml.py -i examples/*.xml -o output/
```

---

## Tags traduisibles

Le script traduit uniquement certains tags principaux selon le type de question. La configuration est définie dans le dictionnaire `tags_a_traduire_par_type` :

```python
tags_a_traduire_par_type = {
    "coderunner"  : question_tags + general_feedback,
    "matching"    : question_tags + general_feedback + partial_feedbacks,
    "multichoice" : question_tags + general_feedback + partial_feedbacks,
    "shortanswer" : question_tags + general_feedback + partial_feedbacks,
    "numerical"   : question_tags + general_feedback,
    "category"    : category_tags
}
```

> 🔹 Pour l’instant, le script **ne traduit pas les réponses**, seulement les tags principaux.
> 🔹 Le dictionnaire permet de contrôler quels tags seront traduits.

---

## Remarques

* Le script est une première version rapide, mais fonctionne déjà pour un cas d’usage réel.
* L'objectif est d'utiliser `xml2xml` pour automatiser la traduction de questions dans des module d'enseignement réel, 
  puis de continuer le développement pour plus de flexibilité.

---

## Exemple de commande complète

```bash
python3 bin/xml2xml.py -i examples/*.xml -o translations/
```

Cette commande traduit tous les fichiers XML du répertoire `examples/` et enregistre les fichiers traduits dans `translations/`.

---

## Contribution

N'hésitez pas à proposer des améliorations ou à adapter la fonction de traduction si vous utilisez un service différent de Google Cloud.

