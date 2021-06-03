# Web-Search-Engine

### Objective
Create a search engine to perform on a collection of ~56,000 unique crawled web pages under the UCI domain with a reponse time of under 300ms.

### Structure
- Inverted Index
  - Tokens: All alphanumeric sequences
  - Porter Stemming: Better textual matches

### Ranking System
Uses TF-IDF scoring to take important words into consideration

### The Search
At the time of the query, the program stems the query terms, looks up the index, and performs a ranking calculation to return relevant pages for the query

### Operational Constraints
Cloud servers/containers that run search engines don’t have a lot of
memory, but they need to handle large amounts of data. To combat this and deal with large amounts of data, the indexer offloads the inverted index hash map from main memory to a
partial index on disk at least 3 times during index construction which are then merged at the end
