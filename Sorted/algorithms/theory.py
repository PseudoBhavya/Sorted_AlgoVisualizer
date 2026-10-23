"""
Sorted — DAA Theory & Algorithm Properties
===========================================
Provides educational theory modules and conceptual references for:
- Properties of Algorithm (Input, Output, Definiteness, Finiteness, Effectiveness, Correctness)
- Dependence and Independence Concepts (Data dependencies, Bernstein's conditions, Parallelism vs Serial execution)
"""

class DAATheoryRegistry:
    """Registry providing theoretical explanations and MSE topics."""

    PROPERTIES_OF_ALGORITHM = {
        "title": "Properties of Algorithm",
        "description": "Fundamental criteria that every well-defined computational algorithm must satisfy.",
        "properties": [
            {
                "name": "Input",
                "definition": "An algorithm must have zero or more well-defined inputs supplied externally before or during execution."
            },
            {
                "name": "Output",
                "definition": "An algorithm must produce at least one output that has a specified relation to the inputs."
            },
            {
                "name": "Definiteness",
                "definition": "Each instruction in an algorithm must be clear, unambiguous, and precisely defined."
            },
            {
                "name": "Finiteness",
                "definition": "An algorithm must terminate after a finite number of execution steps for any valid input."
            },
            {
                "name": "Effectiveness",
                "definition": "Every operation must be basic enough to be carried out exactly and in a finite amount of time using pencil and paper."
            },
            {
                "name": "Correctness",
                "definition": "An algorithm must yield the correct computational output for all valid input instances."
            }
        ]
    }

    DEPENDENCE_INDEPENDENCE = {
        "title": "Dependence and Independence Concepts",
        "description": "Analysis of data dependencies and execution independence in sequential and parallel algorithm design.",
        "concepts": [
            {
                "name": "Data Dependence (RAW - Read After Write)",
                "definition": "Statement S2 depends on S1 if S1 writes a variable that S2 subsequently reads. Requires sequential execution order."
            },
            {
                "name": "Anti-Dependence (WAR - Write After Read)",
                "definition": "Statement S2 has anti-dependence on S1 if S1 reads a variable that S2 subsequently overwrites."
            },
            {
                "name": "Output Dependence (WAW - Write After Write)",
                "definition": "Statement S2 has output dependence on S1 if both S1 and S2 write to the same memory location."
            },
            {
                "name": "Independent Subproblems (Divide & Conquer)",
                "definition": "In algorithms like Merge Sort and Divide-and-Conquer Min-Max, recursive subproblems operate on disjoint memory slices and can execute concurrently without synchronization overhead."
            }
        ]
    }

    @classmethod
    def get_all_theory(cls) -> dict:
        return {
            "properties": cls.PROPERTIES_OF_ALGORITHM,
            "dependence": cls.DEPENDENCE_INDEPENDENCE
        }
