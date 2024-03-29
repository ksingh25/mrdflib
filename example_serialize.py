from rdflib import Graph, Literal, BNode, RDF
from rdflib.namespace import FOAF, DC

if __name__ == "__main__":

    store = Graph()

    # Bind a few prefix, namespace pairs for pretty output
    store.bind("dc", DC)
    store.bind("foaf", FOAF)

    # Create an identifier to use as the subject for Donna.
    donna = BNode()

    # Add triples using store's add method.
    store.add((donna, RDF.type, FOAF.Person))
    store.add((donna, FOAF.nick, Literal("donna", "foo")))
    store.add((donna, FOAF.name, Literal("Donna Fales")))

    jack = BNode()
    # Add triples using store's add method.
    store.add((jack, RDF.type, FOAF.Person))
    store.add((jack, FOAF.nick, Literal("jack", "en")))
    store.add((jack, FOAF.name, Literal("Jack Jack")))


    # Iterate over triples in store and print them out.
    print("--- printing raw triples ---")
    for s, p, o in store:
        print(s, p, o)

    # For each foaf:Person in the store print out its mbox property.
    print()
    print("--- printing mboxes ---")
    for person in store.subjects(RDF.type, FOAF["Person"]):
        for mbox in store.objects(person, FOAF["mbox"]):
            print(mbox)

    #print("--- saving RDF to a file (donna_foaf.rdf) ---")
    # Serialize the store as RDF/XML to the file donna_foaf.rdf.
    ##store.serialize("donna_foaf.rdf", format="pretty-xml", max_depth=3)

    # Let's show off the serializers
    print()
    print("RDF Serializations:")

    # Serialize as Turtle (default)
    print("--- start: turtle ---")
    print(store.serialize(None, "turtle"))
    print("--- end: turtle ---\n")

    # Serialize as XML
    #print("--- start: rdf-xml ---")
    #print(store.serialize(None, "pretty-xml"))
    #print("--- end: rdf-xml ---\n")

    
    # Serialize as NTriples
    print("--- start: ntriples ---")
    print(store.serialize(None,"nt"))
    print("--- end: ntriples ---\n")

    # Serialize as JSON-LD
    # only if you have the JSON-LD plugin installed!
    print("--- start: JSON-LD ---")
    print(store.serialize(None,"json-ld"))
    print("--- end: JSON-LD ---\n")
    
