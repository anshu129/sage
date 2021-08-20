"""
Elliptic-curve morphisms

This class serves as a common parent for various specializations
of morphisms between elliptic curves. In the future, some of the
code currently contained in the EllipticCurveIsogeny class should
be moved here, and new code for cases not currently covered by the
EllipticCurveIsogeny class should inherit from this class in order
to eventually provide a uniform interface for all elliptic-curve
maps --- regardless of differences in internal representations.
"""

from sage.categories.morphism import Morphism

class EllipticCurveHom(Morphism):
    """
    Base class for elliptic-curve morphisms.
    """

    def _repr_type(self):           # used by Morphism._repr_
        return 'Elliptic-curve'

    @staticmethod
    def _composition_impl(left, right):
        """
        Called by :meth:`_composition_`.
        """
        raise NotImplementedError('subclasses should implement _composition_impl')

    def _composition_(self, other, homset):
        """
        Return the composition of this elliptic-curve morphism
        with another elliptic-curve morphism.

        EXAMPLES::

            sage: E = EllipticCurve(GF(19), [1,0])
            sage: phi = E.isogeny(E(0,0))
            sage: iso = E.change_weierstrass_model(5,0,0,0).isomorphism_to(E)
            sage: phi * iso
            Isogeny of degree 2 from Elliptic Curve defined by y^2 = x^3 + 9*x over Finite Field of size 19 to Elliptic Curve defined by y^2 = x^3 + 15*x over Finite Field of size 19
            sage: phi.dual() * phi
            Composite map:
              From: Elliptic Curve defined by y^2 = x^3 + x over Finite Field of size 19
              To:   Elliptic Curve defined by y^2 = x^3 + x over Finite Field of size 19
              Defn:   Isogeny of degree 2 from Elliptic Curve defined by y^2 = x^3 + x over Finite Field of size 19 to Elliptic Curve defined by y^2 = x^3 + 15*x over Finite Field of size 19
                    then
                      Isogeny of degree 2 from Elliptic Curve defined by y^2 = x^3 + 15*x over Finite Field of size 19 to Elliptic Curve defined by y^2 = x^3 + x over Finite Field of size 19
        """
        if not isinstance(self, EllipticCurveHom) or not isinstance(other, EllipticCurveHom):
            raise TypeError(f'cannot compose {type(self)} with {type(other)}')

        try:
            return self._composition_impl(self, other)
        except NotImplementedError:
            pass

        try:
            return other._composition_impl(self, other)
        except NotImplementedError:
            pass

        # fall back to generic formal composite map
        return Morphism._composition_(self, other, homset)

