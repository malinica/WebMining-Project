# Going Seventeen – YouTube Comment Topic Modeling 📺🔍

## Introduction

This project applies topic modeling to English-language YouTube comments from the **Going Seventeen** variety show, with a focus on detecting **fan wish comments** - comments in which viewers express what they would like to see in future episodes.

The notebook demonstrates a complete NLP pipeline: data loading and text analysis, regex-based wish comment filtering, text preprocessing, topic modeling with LDA, NMF, and BERTopic, and a comparative evaluation of model variants.

## Methodology

### Exploratory Data Analysis (EDA)

- Analyzed comment distribution across recent vs. popular episodes
- Visualized comment length distributions (character count, word count, sentence count)
- Computed vocabulary size and lexical diversity (Type-Token Ratio)
- Identified top 30 most frequent tokens and generated word clouds

### Wish Comment Filtering

- Applied a custom regex pattern set (50+ patterns) to isolate comments expressing wishes, suggestions, or expectations
- Patterns grouped into: direct wishes, suggestions, nostalgia/bring-back, expectations, episode ideas, and direct requests
- Evaluated filtering quality through manual inspection of sampled wish and non-wish comments, and per-pattern hit counts

### Wish Comment Classification

- Keyword-based categorization into 7 predefined categories: Games and Activity, Talk Show, Group Dynamic, Emotions, Travelling, Music and Performance, Repeated Format
- Used as a baseline for comparison with topic models
- Uncategorized ("Other") comments analyzed separately using BERTopic for sub-topic discovery

### Text Preprocessing

- Normalization (lowercasing, punctuation removal, URL/HTML stripping)
- Tokenization
- Stop word removal (with domain-specific wish-stop words)
- Lemmatization (WordNetLemmatizer)

### Topic Modeling

**LDA** - Latent Dirichlet Allocation via scikit-learn; bag-of-words representation with CountVectorizer

**NMF** - Non-negative Matrix Factorization via scikit-learn; TF-IDF representation

**BERTopic - Variant A** – Sentence Transformers embeddings (`all-MiniLM-L6-v2`) + UMAP dimensionality reduction + HDBSCAN clustering + c-TF-IDF topic representation

**BERTopic - Variant B** – Word2Vec document embeddings (averaged word vectors) as an alternative to Sentence Transformers

### Model Comparison

- Quantitative evaluation: coherence scores, silhouette scores, number of topics discovered, noise ratio (outlier comments)
- Qualitative evaluation: UMAP 2D embedding geometry, semantic precision of topic clusters, representative comment inspection
- Analysis of wish topics broken down by group member mentions and episode type (popular vs. recent)

## Results

- BERTopic Variant A produced the most semantically coherent and granular topic clusters
- LDA and NMF identified broader, overlapping themes but were less precise on short informal text
- Fan wishes predominantly fell into Games and Activity and Repeated Format categories
- Wish comments were more frequently found in popular episode threads than recent ones

## Tech Stack

- **Topic Modeling:** `bertopic`, `scikit-learn` (LDA, NMF), `gensim` (Word2Vec, CoherenceModel)
- **Embeddings:** `sentence-transformers`, `umap-learn`, `hdbscan`
- **NLP:** `nltk` (tokenization, stop words, lemmatization)
- **Data Collection:** `google-api-python-client`, YouTube Data API v3
- **Data Processing:** `pandas`, `numpy`
- **Visualization:** `matplotlib`, `seaborn`, `wordcloud`, `plotly`
