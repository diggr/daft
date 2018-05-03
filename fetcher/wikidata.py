import SPARQLWrapper

ALL_GAMES_QUERY = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?game 
       (SAMPLE(?label_en) AS ?label_en) 
       (SAMPLE(?label_ja) AS ?label_ja) 
       (SAMPLE(?label_de) AS ?label_de) 
       (SAMPLE(?pl_label) AS ?platform_label)
WHERE 
{
  ?game wdt:P31 wd:Q7889.
  ?game wdt:P400 ?platform.
  ?platform rdfs:label ?pl_label
  FILTER (LANG(?pl_label) = "en" ).
  OPTIONAL {  
    ?game rdfs:label ?label_en
    FILTER (LANG (?label_en) = "en" ).
   }
  OPTIONAL {  
    ?game rdfs:label ?label_ja
    FILTER (LANG (?label_ja) = "ja" ).
   }
  OPTIONAL {  
    ?game rdfs:label ?label_de
    FILTER (LANG (?label_de) = "de" ).
   }  
}
GROUP BY ?game ?platform
"""