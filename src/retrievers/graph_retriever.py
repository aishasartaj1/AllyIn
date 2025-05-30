from neo4j import GraphDatabase

# Neo4j credentials
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "allyin123"

# Connect to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def run_cypher_query(query):
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

def safe_get(record, key):
    return record.get(key, "<unknown>")

if __name__ == "__main__":
    # === Facilities that exceed regulations ===
    print("🔎 Facilities that exceed regulations:\n")
    cypher = """
    MATCH (f:Facility)-[:EXCEEDS]->(r:Regulation)
    RETURN f.name AS facility, r.name AS regulation
    """
    results = run_cypher_query(cypher)
    for row in results:
        print(f"- {safe_get(row, 'facility')} exceeds {safe_get(row, 'regulation')}")

    # === Compliance Officers per Facility ===
    print("\n🔎 Compliance Officers per Facility:\n")
    cypher = """
    MATCH (f:Facility)-[rel:REL]->(e:Entity)
    WHERE toLower(e.name) CONTAINS 'compliance'
    RETURN f.name AS facility, e.name AS officer
    """
    results = run_cypher_query(cypher)
    if not results:
        print("⚠️ No compliance officer data found.")
    for row in results:
        print(f"- {safe_get(row, 'officer')} is responsible for {safe_get(row, 'facility')}")

    # === Documents mentioning regulations ===
    print("\n🔎 Documents mentioning regulations:\n")
    cypher = """
    MATCH (d:Entity)-[rel:REL]->(r:Regulation)
    RETURN d.name AS document, r.name AS regulation
    """
    results = run_cypher_query(cypher)
    if not results:
        print("⚠️ No document-regulation references found.")
    for row in results:
        print(f"- '{safe_get(row, 'document')}' mentions regulation '{safe_get(row, 'regulation')}'")
