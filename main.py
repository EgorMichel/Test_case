import math

class Vertex:
    def __init__(self):
        self.atr          = None
        self.income_edges = []
        self.rule         = None
        self.copy_target  = None

    def proceed(self):
        if self.rule == "copy":
            if self.Copy():
                self.rule = None
        elif self.rule == "min":
            if self.Min():
                self.rule = None

    def Min(self):
        try:
            self.atr = min([edge.atr for edge in self.income_edges])
            return True
        except:
            for edge in self.income_edges:
                edge.proceed()
            return False

    def Copy(self):
        if self.copy_target.atr:
            self.atr = self.copy_target.atr
            return True
        else:
            self.copy_target.proceed()
            return False


class Edge:
    def __init__(self):
        self.atr           = None
        self.parent_vertex = None
        self.rule          = None
        self.copy_target   = None

    def proceed(self):
        if self.rule == "copy":
            if self.Copy():
                self.rule = None
        elif self.rule == "mul":
            if self.Mul():
                self.rule = None

    def Mul(self):
        try:
            self.atr = self.parent_vertex.atr * math.prod([edge.atr for edge in self.parent_vertex.income_edges])
            return True
        except:
            self.parent_vertex.proceed()
            for edge in self.parent_vertex.income_edges:
                edge.proceed()
            return False

    def Copy(self):
        if self.copy_target.atr:
            self.atr = self.copy_target.atr
            return True
        else:
            self.copy_target.proceed()
            return False



def Proceed_file(read, write):

    with open(read, 'r') as f:
        lines = f.readlines()

    # First Line
    first_line = lines[0].strip()
    if first_line:
        parts = first_line.split('#')[0].strip().split()
        NV = int(parts[0])
        NE = int(parts[1])
    else:
        raise ValueError("Первая строка файла должна содержать количество узлов и ребер.")

    vertex = [Vertex() for i in range(NV)]
    edges  = [Edge()   for i in range(NE)]

    # Filling vertexes and edges
    for i in range(NE):
        line = lines[i+2].strip()
        if line:
            parts = line.split('#')[0].strip().split()
            first  = int(parts[0]) - 1
            second = int(parts[1]) - 1
            edges[i].parent_vertex = vertex[first]
            vertex[second].income_edges.append(edges[i])
        else:
            raise ValueError("Список ребер должен быть полным.")


    # Applying rules for Vertexes
    for i in range(NV):
        line = lines[i + 3 + NE].strip()
        if line:
            parts = line.split('#')[0].strip().split()

            if len(parts) == 2: # Copy case
                vertex[i].rule = "copy"
                if parts[0] == 'v': # Vertex case
                    vertex[i].copy_target = vertex[int(parts[1]) - 1]
                if parts[0] == 'e': # Edge case
                    vertex[i].copy_target = edges [int(parts[1]) - 1]

            elif parts[0] == "min":
                vertex[i].rule = "min"
            else:
                vertex[i].atr = float(parts[0])
        else:
            raise ValueError("Список правил для вершин не должен содержать пустых строк.")

    # Applying rules for Edges
    for i in range(NE):
        line = lines[i + 3 + NE + NV].strip()
        if line:
            parts = line.split('#')[0].strip().split()

            if len(parts) == 2:  # Swap case
                edges[i].rule = "copy"
                if parts[0] == 'v':  # Vertex case
                    edges[i].copy_target = vertex[int(parts[1]) - 1]
                if parts[0] == 'e':  # Edge case
                    edges[i].copy_target = edges [int(parts[1]) - 1]
            elif parts[0] == "*":
                edges[i].rule = "mul"
            else:
                edges[i].atr = float(parts[0])
        else:
            raise ValueError("Список правил для ребер не должен содержать пустых строк.")


    # Processing rules while no ambiguities
    while None in [v.atr for v in vertex] or None in [e.atr for e in edges]:
        for v in vertex:
            v.proceed()
        for e in edges:
            e.proceed()

    with open(write, "w") as f:
        for v in vertex:
            num = int(v.atr) if v.atr.is_integer() else float(v.atr)
            f.write(f"{num}\n")
        for e in edges:
            num = int(e.atr) if e.atr.is_integer() else float(e.atr)
            f.write(f"{num}\n")


if __name__ == "__main__":
    Proceed_file(input(), input())



