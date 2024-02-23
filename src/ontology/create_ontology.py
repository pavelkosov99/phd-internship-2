from owlready2 import *
import os


def ontology_builder(output_path):
    onto = get_ontology("http://example.org/ontology#")

    with onto:
        # Main Digit Class
        class Clothes(Thing):
            pass

        # Main Property Class
        class Properties(Thing):
            pass

        # Main Property subclasses
        # BodyPart and its Subclasses
        class BodyPart(Properties):
            pass

        class WholeBody(BodyPart):
            pass

        class TopPart(BodyPart):
            pass

        class BottomPart(BodyPart):
            pass

        class Feet(BodyPart):
            pass

        class Hands(BodyPart):
            pass

        # Weather Subclasses
        class WeatherType(Properties):
            pass

        class Cold(WeatherType):
            pass

        class Warm(WeatherType):
            pass

        class Any(WeatherType):
            pass

        # EdgeShape Subclasses
        class EdgeShape(Properties):
            pass

        class StraightEdge(EdgeShape):
            pass

        class CurveEdge(EdgeShape):
            pass

        # Explanatory Properties and its subproperty
        class ExplanatoryProperty(ObjectProperty):
            pass

        class hasBodyPart(ExplanatoryProperty):
            domain = [Clothes]
            range = [BodyPart]

        class hasWeatherType(ExplanatoryProperty):
            domain = [Clothes]
            range = [WeatherType]

        class hasEdgeShape(ExplanatoryProperty):
            domain = [Clothes]
            range = [EdgeShape]

        # Clothing subclasses
        class TshirtTop(Clothes):
            is_a = [
                hasBodyPart.some(TopPart) &
                hasWeatherType.some(Warm) &
                hasEdgeShape.some(CurveEdge) &
                Not(hasBodyPart.some(WholeBody)) &
                Not(hasBodyPart.some(BottomPart)) &
                Not(hasBodyPart.some(Feet)) &
                Not(hasBodyPart.some(Hands)) &
                Not(hasWeatherType.some(Cold)) &
                Not(hasWeatherType.some(Any)) &
                Not(hasEdgeShape.some(StraightEdge))
            ]

        class Trouser(Clothes):
            is_a = [
                hasBodyPart.some(BottomPart) &
                hasWeatherType.some(Any) &
                hasEdgeShape.some(StraightEdge) &
                Not(hasBodyPart.some(WholeBody)) &
                Not(hasBodyPart.some(TopPart)) &
                Not(hasBodyPart.some(Feet)) &
                Not(hasBodyPart.some(Hands)) &
                Not(hasWeatherType.some(Cold)) &
                Not(hasWeatherType.some(Warm)) &
                Not(hasEdgeShape.some(CurveEdge))
            ]

        class Pullover(Clothes):
            is_a = [
                hasBodyPart.some(TopPart) &
                hasWeatherType.some(Cold) &
                hasEdgeShape.some(CurveEdge) &
                Not(hasBodyPart.some(WholeBody)) &
                Not(hasBodyPart.some(BottomPart)) &
                Not(hasBodyPart.some(Feet)) &
                Not(hasBodyPart.some(Hands)) &
                Not(hasEdgeShape.some(StraightEdge)) &
                Not(hasWeatherType.some(Any)) &
                Not(hasWeatherType.some(Warm))
            ]

        class Dress(Clothes):
            is_a = [
                hasBodyPart.some(WholeBody) &
                hasWeatherType.some(Any) &
                hasEdgeShape.some(StraightEdge) &
                Not(hasWeatherType.some(Cold)) &
                Not(hasWeatherType.some(Warm)) &
                Not(hasEdgeShape.some(CurveEdge)) &
                Not(hasBodyPart.some(TopPart)) &
                Not(hasBodyPart.some(BottomPart)) &
                Not(hasBodyPart.some(Feet)) &
                Not(hasBodyPart.some(Hands))
            ]

        class Coat(Clothes):
            is_a = [
                hasBodyPart.some(TopPart) &
                hasWeatherType.some(Cold) &
                hasEdgeShape.some(CurveEdge) &
                Not(hasBodyPart.some(WholeBody)) &
                Not(hasBodyPart.some(BottomPart)) &
                Not(hasBodyPart.some(Feet)) &
                Not(hasBodyPart.some(Hands)) &
                Not(hasEdgeShape.some(StraightEdge)) &
                Not(hasWeatherType.some(Any)) &
                Not(hasWeatherType.some(Warm))
            ]

        class Sandal(Clothes):
            is_a = [
                hasBodyPart.some(Feet) &
                hasWeatherType.some(Warm) &
                hasEdgeShape.some(StraightEdge) &
                Not(hasWeatherType.some(Cold)) &
                Not(hasWeatherType.some(Any)) &
                Not(hasEdgeShape.some(CurveEdge)) &
                Not(hasBodyPart.some(TopPart)) &
                Not(hasBodyPart.some(BottomPart)) &
                Not(hasBodyPart.some(WholeBody)) &
                Not(hasBodyPart.some(Hands))
            ]

        class Shirt(Clothes):
            is_a = [
                hasBodyPart.some(TopPart) &
                hasWeatherType.some(Any) &
                hasEdgeShape.some(CurveEdge) &
                Not(hasBodyPart.some(WholeBody)) &
                Not(hasBodyPart.some(BottomPart)) &
                Not(hasBodyPart.some(Feet)) &
                Not(hasBodyPart.some(Hands)) &
                Not(hasEdgeShape.some(StraightEdge)) &
                Not(hasWeatherType.some(Cold)) &
                Not(hasWeatherType.some(Warm))
            ]

        class Sneaker(Clothes):
            is_a = [
                hasBodyPart.some(Feet) &
                hasWeatherType.some(Any) &
                hasEdgeShape.some(CurveEdge) &
                Not(hasEdgeShape.some(StraightEdge)) &
                Not(hasWeatherType.some(Cold)) &
                Not(hasWeatherType.some(Warm)) &
                Not(hasBodyPart.some(TopPart)) &
                Not(hasBodyPart.some(BottomPart)) &
                Not(hasBodyPart.some(WholeBody)) &
                Not(hasBodyPart.some(Hands))
            ]

        class Bag(Clothes):
            is_a = [
                hasBodyPart.some(Hands) &
                hasWeatherType.some(Any) &
                hasEdgeShape.some(StraightEdge) &
                Not(hasWeatherType.some(Cold)) &
                Not(hasWeatherType.some(Warm)) &
                Not(hasEdgeShape.some(CurveEdge)) &
                Not(hasBodyPart.some(TopPart)) &
                Not(hasBodyPart.some(BottomPart)) &
                Not(hasBodyPart.some(Feet)) &
                Not(hasBodyPart.some(WholeBody))
            ]

        class AnkleBoot(Clothes):
            is_a = [
                hasBodyPart.some(Feet) &
                hasWeatherType.some(Cold) &
                hasEdgeShape.some(StraightEdge) &
                Not(hasEdgeShape.some(CurveEdge)) &
                Not(hasWeatherType.some(Any)) &
                Not(hasWeatherType.some(Warm)) &
                Not(hasBodyPart.some(TopPart)) &
                Not(hasBodyPart.some(BottomPart)) &
                Not(hasBodyPart.some(WholeBody)) &
                Not(hasBodyPart.some(Hands))
            ]

        try:
            sync_reasoner()
            onto.save(output_path, format="rdfxml")
            return True
        except OwlReadyInconsistentOntologyError as error:
            return error


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "../../data/ontology/ontology.owl")
    ontology_builder(output_path)


if __name__ == "__main__":
    main()
