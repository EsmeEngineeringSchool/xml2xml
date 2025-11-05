# xml2xml

`xml2xml` est un outil en ligne de commande écrit en Python permettant 
de **traduire automatiquement des fichiers XML Moodle** 
(par exemple des banques de questions) en ciblant des balises spécifiques 
selon le type de question.  
Il s'appuie sur le module [`lxml`](https://lxml.de/) pour la manipulation 
des fichiers XML et sur l'API 
[`google-cloud-translate`](https://cloud.google.com/translate/docs) pour la traduction automatique.

Ce dépôt inclut également un utilitaire complémentaire, 
[`merge_xml`](#merge_xml), pour fusionner plusieurs fichiers XML traduits ou non en un seul 
au sein d'une arborescence de fichiers.

---

## Installation

1. **Cloner le dépôt**

```bash
git clone <URL_DU_DEPOT>
cd <REPERTOIRE_DU_DEPOT>
```


## Dépendances 

> ⚠️ L'utilisation de la fonction `translate_text()` nécessite une configuration valide du SDK Google Cloud.  
> Vous pouvez remplacer cette fonction par un autre service de traduction si vous le souhaitez (DeepL, LibreTranslate, etc.).

---

## Utilisation

### Traduction de fichiers XML

Pour traduire un ou plusieurs fichiers XML :

```bash
python3 bin/xml2xml.py -i examples/*.xml
```

Par défaut, les fichiers traduits sont enregistrés dans le répertoire courant.

Exemple de sortie :

```
examples/coderunner.xml    -> ./coderunner_en.xml
examples/matching.xml      -> ./matching_en.xml
examples/multichoice.xml   -> ./multichoice_en.xml
examples/numerical.xml     -> ./numerical_en.xml
examples/shortanswer.xml   -> ./shortanswer_en.xml
```

### Définir un répertoire de sortie

Il est possible de spécifier un dossier de sortie à l'aide de l'option `-o` :

```bash
python3 bin/xml2xml.py -i examples/*.xml -o translations/
```

---

## Tags traduisibles

Le script traduit uniquement certains tags selon le type de question Moodle.  
Ces règles sont définies dans le dictionnaire `tags_a_traduire_par_type` du fichier `xml2xml.py` :

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

> 🔹 Le script **ne traduit pas les réponses**, uniquement les intitulés, énoncés et feedbacks.  
> 🔹 Le dictionnaire peut être modifié pour adapter la traduction à d'autres balises.

---

## merge_xml

Le dépôt contient également un second script : **`merge_xml.py`**.  
Il permet de **fusionner plusieurs fichiers XML Moodle** 
(par exemple ceux traduits avec `xml2xml`) en un seul fichier prêt à être importé dans Moodle.

### Exemple d'utilisation

```bash
python3 bin/merge_xml.py <repertoire>
```

Le script parcourt récursivement le répertoire indiqué, 
fusionne tous les fichiers XML qu'il contient, et crée un fichier `<repertoire>.xml` en chaque noeud.  
Chaque fichier est intégré à l'intérieur d'une balise `<quiz>...</quiz>` complète.

---

## Exemple de workflow complet

1. **Traduire tous les fichiers XML**

```bash
python3 bin/xml2xml.py -i examples/*.xml -o translated/
```

2. **Fusionner les fichiers traduits**

```bash
python3 bin/merge_xml.py translated/
```

Résultat : un fichier unique `translated.xml` contenant l'ensemble des questions traduites, prêt pour l'import Moodle.

---

## TODO 

Les contributions sont les bienvenues.  
Axes d'amélioration possibles :

- Détection automatique des balises à traduire  
- Gestion plus fine des CDATA et encodages  
- Support d'autres API de traduction  
- Ajout d'options CLI (choix de langue, etc.)

---

## Licence

Ce projet est distribué sous licence libre (voir le fichier `LICENSE` pour plus de détails).

