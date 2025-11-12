# xml2xml

`xml2xml` est un outil en ligne de commande en Python permettant de **traduire automatiquement des fichiers XML Moodle** (banques de questions, quiz, etc.)  
en ciblant des balises spécifiques selon le type de question.

Il s'appuie sur le module [`lxml`](https://lxml.de/) pour la manipulation des fichiers XML et offre deux moteurs de traduction :

- **[LibreTranslate](https://libretranslate.com/)** (par défaut, via un serveur local ou distant)
- **[Google Cloud Translate](https://cloud.google.com/translate/docs)** (optionnel, via le SDK officiel)

Ce dépôt inclut également un utilitaire complémentaire [`merge_xml`](#merge_xml) permettant de **fusionner plusieurs fichiers XML** traduits ou non.

---
> ATTENTION: L'utilisation de l'API Google Cloud nécessite une configuration valide du SDK (clé d'API et variable d'environnement `GOOGLE_APPLICATION_CREDENTIALS`).  
> Si aucun moteur n'est spécifié, `xml2xml` utilisera **LibreTranslate** par défaut (attendu sur `http://localhost:5000/translate`).

---

## 🚀 Utilisation

### Traduire un ou plusieurs fichiers XML

```bash
python3 bin/xml2xml.py -i examples/*.xml
```

Par défaut :
- la **langue cible** est `en` (anglais),
- le **moteur de traduction** est `libretranslate`,
- les fichiers traduits sont enregistrés dans le répertoire courant.

Exemple de sortie :

```
examples/coderunner.xml    -> ./coderunner_en.xml
examples/matching.xml      -> ./matching_en.xml
examples/multichoice.xml   -> ./multichoice_en.xml
examples/numerical.xml     -> ./numerical_en.xml
examples/shortanswer.xml   -> ./shortanswer_en.xml
```

---

### Définir la langue cible

```bash
python3 bin/xml2xml.py -i examples/*.xml -t pt
```

Traduit les fichiers XML vers le **portugais**.

---

### Spécifier le moteur de traduction

#### Utiliser LibreTranslate (par défaut)

```bash
python3 bin/xml2xml.py -i examples/*.xml -l
```

LibreTranslate doit être accessible localement sur :

```
http://localhost:5000/translate
```

#### Utiliser Google Cloud Translate

```bash
python3 bin/xml2xml.py -i examples/*.xml -g
```

Cette option nécessite que ton environnement Google Cloud soit configuré correctement.

---
### Définir un répertoire de sortie

```bash
python3 bin/xml2xml.py -i examples/*.xml -o translations/
```

Tous les fichiers traduits seront créés dans le dossier `translations/`.

---

### Fichier de configuration

Tu peux enrichir la liste des **balises à traduire** en fournissant un fichier via `--config` :

```bash
python3 bin/xml2xml.py -i examples/*.xml -c extra_tags
```

Chaque ligne du fichier doit contenir un **XPath** vers un tag supplémentaire à traduire, par exemple :

```
//answers/text
//answer/feedback
```

---

## Tags traduisibles par défaut

Le script traduit uniquement certains tags selon le type de question Moodle.  
Ces règles sont définies dans le dictionnaire `tags_a_traduire_par_type` du fichier `xml2xml.py` :

```python
tags_a_traduire_par_type = {
    "coderunner"       : question_tags + general_feedback,
    "matching"         : question_tags + general_feedback + partial_feedbacks,
    "multichoice"      : question_tags + general_feedback + partial_feedbacks,
    "shortanswer"      : question_tags + general_feedback + partial_feedbacks,
    "shortanswerwiris" : question_tags + general_feedback,
    "numerical"        : question_tags + general_feedback,
    "category"         : category_tags
}
```

> Les balises `<name>` et `<questiontext>` sont toujours traduites.  
> Le contenu `<questiontext>` est automatiquement réécrit en CDATA si nécessaire.  
> Les réponses ne sont pas traduites (par défaut).

---

## merge_xml

Le dépôt contient également un second script : **`merge_xml.py`**.  
Il permet de **fusionner plusieurs fichiers XML Moodle** (traduit ou non) en un seul fichier global prêt à être importé dans Moodle.

### Exemple d'utilisation

```bash
python3 bin/merge_xml.py <repertoire>
```

Le script parcourt récursivement le répertoire indiqué, fusionne tous les fichiers XML qu'il contient et crée un fichier `<repertoire>.xml` à la racine.  
Chaque fichier est intégré à l'intérieur d'une balise `<quiz>...</quiz>` complète.

---

## Améliorations possibles

- Support d'autres moteurs de traduction (DeepL, OpenAI, etc.)  
- Détection automatique de la langue source  
- Meilleure gestion des CDATA et des balises complexes  
