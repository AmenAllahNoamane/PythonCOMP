
class Automate:
    def __init__(self, initial, final, transitions):
        self.initial = initial
        self.final = final
        self.transitions = transitions


class Thompson:
    def __init__(self):
        self.numero = 0

    def nouvel_etat(self):
        etat = self.numero
        self.numero = self.numero + 1
        return etat

    def symbole(self, c):
        debut = self.nouvel_etat()
        fin = self.nouvel_etat()

        transitions = [(debut, c, fin)]

        return Automate(debut, fin, transitions)

    def mot_vide(self):
        debut = self.nouvel_etat()
        fin = self.nouvel_etat()

        transitions = [(debut, "ε", fin)]

        return Automate(debut, fin, transitions)

    def concatener(self, a, b):
        transitions = a.transitions + b.transitions

        transitions.append(
            (a.final, "ε", b.initial)
        )

        return Automate(
            a.initial,
            b.final,
            transitions
        )

    def union(self, a, b):
        debut = self.nouvel_etat()
        fin = self.nouvel_etat()

        transitions = a.transitions + b.transitions

        transitions.append((debut, "ε", a.initial))
        transitions.append((debut, "ε", b.initial))
        transitions.append((a.final, "ε", fin))
        transitions.append((b.final, "ε", fin))

        return Automate(debut, fin, transitions)

    def etoile(self, a):
        debut = self.nouvel_etat()
        fin = self.nouvel_etat()

        transitions = a.transitions.copy()

        transitions.append((debut, "ε", a.initial))
        transitions.append((debut, "ε", fin))
        transitions.append((a.final, "ε", a.initial))
        transitions.append((a.final, "ε", fin))

        return Automate(debut, fin, transitions)

    def plus(self, a):
        debut = self.nouvel_etat()
        fin = self.nouvel_etat()

        transitions = a.transitions.copy()

        transitions.append((debut, "ε", a.initial))
        transitions.append((a.final, "ε", a.initial))
        transitions.append((a.final, "ε", fin))

        return Automate(debut, fin, transitions)

    def optionnel(self, a):
        debut = self.nouvel_etat()
        fin = self.nouvel_etat()

        transitions = a.transitions.copy()

        transitions.append((debut, "ε", a.initial))
        transitions.append((debut, "ε", fin))
        transitions.append((a.final, "ε", fin))

        return Automate(debut, fin, transitions)


if __name__ == "__main__":
    th = Thompson()

    a = th.symbole("a")
    b = th.symbole("b")

    ab = th.concatener(a, b)

    print("Etat initial :", ab.initial)
    print("Etat final :", ab.final)

    print("Transitions :")
    for t in ab.transitions:
        print(t)
