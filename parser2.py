
from lexer import analyse_lexicale
from automate import Thompson


class Parser:
    def __init__(self, expression):
        self.tokens = analyse_lexicale(expression)
        self.pos = 0
        self.th = Thompson()

    def courant(self):
        return self.tokens[self.pos]

    def avancer(self):
        if self.pos < len(self.tokens) - 1:
            self.pos = self.pos + 1

    def erreur(self, attendu):
        t = self.courant()

        raise SyntaxError(
            "Erreur a la position " + str(t.position)
            + " : " + attendu
            + " attendu, " + t.nature + " trouve"
        )

    def accepter(self, nature):
        if self.courant().nature == nature:
            self.avancer()
        else:
            self.erreur(nature)

    def analyser(self):
        resultat = self.R()

        if self.courant().nature != "FIN":
            self.erreur("FIN")

        return resultat

    def R(self):
        a = self.T()
        return self.R_prime(a)

    def R_prime(self, h):
        if self.courant().nature == "UNION":
            self.avancer()

            b = self.T()
            resultat = self.th.union(h, b)

            return self.R_prime(resultat)

        elif self.courant().nature in [
            "PARENTHESE_FERMANTE",
            "FIN"
        ]:
            return h

        else:
            self.erreur("UNION, ) ou FIN")

    def T(self):
        a = self.F()
        return self.T_prime(a)

    def T_prime(self, h):
        if self.courant().nature in [
            "SYMBOLE",
            "MOT_VIDE",
            "PARENTHESE_OUVRANTE"
        ]:
            b = self.F()
            resultat = self.th.concatener(h, b)

            return self.T_prime(resultat)

        elif self.courant().nature in [
            "UNION",
            "PARENTHESE_FERMANTE",
            "FIN"
        ]:
            return h

        else:
            self.erreur("SYMBOLE, @, (, |, ) ou FIN")

    def F(self):
        a = self.A()
        return self.F_prime(a)

    def F_prime(self, h):
        nature = self.courant().nature

        if nature == "ETOILE":
            self.avancer()
            resultat = self.th.etoile(h)
            return self.F_prime(resultat)

        elif nature == "PLUS":
            self.avancer()
            resultat = self.th.plus(h)
            return self.F_prime(resultat)

        elif nature == "OPTIONNEL":
            self.avancer()
            resultat = self.th.optionnel(h)
            return self.F_prime(resultat)

        elif nature in [
            "SYMBOLE",
            "MOT_VIDE",
            "PARENTHESE_OUVRANTE",
            "UNION",
            "PARENTHESE_FERMANTE",
            "FIN"
        ]:
            return h

        else:
            self.erreur("*, +, ?, SYMBOLE, @, (, |, ) ou FIN")

    def A(self):
        nature = self.courant().nature

        if nature == "PARENTHESE_OUVRANTE":
            self.avancer()

            resultat = self.R()

            self.accepter("PARENTHESE_FERMANTE")

            return resultat

        elif nature == "SYMBOLE":
            c = self.courant().valeur
            self.avancer()

            return self.th.symbole(c)

        elif nature == "MOT_VIDE":
            self.avancer()

            return self.th.mot_vide()

        else:
            self.erreur("(, SYMBOLE ou @")


if __name__ == "__main__":
    expressions = [
        "a",
        "ab",
        "a|b",
        "a*",
        "a+",
        "a?",
        "(a|b)*",
        "a|bc*",
        "a||b",
        "(ab"
    ]

    for exp in expressions:
        print("\nExpression :", exp)

        try:
            p = Parser(exp)
            automate = p.analyser()

            print("Expression valide")
            print("Initial :", automate.initial)
            print("Final :", automate.final)

            print("Transitions :")
            for t in automate.transitions:
                print(t)

        except (SyntaxError, ValueError) as e:
            print(e)
