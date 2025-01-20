from typing import Literal

from sqlmodel import Field, SQLModel  # type: ignore


class Cat(SQLModel):
    pet_type: Literal["cat"]
    meows: int


class Dog(SQLModel):
    pet_type: Literal["dog"]
    barks: float


class Lizard(SQLModel):
    pet_type: Literal["reptile", "lizard"]
    scales: bool


class Model(SQLModel):
    pet: Cat | Dog | Lizard = Field(..., discriminator="pet_type")
    n: int


def test_create_pets():
    m = Model(pet={"pet_type": "dog", "barks": 3.14}, n=1)  # type: ignore
    assert m.pet.pet_type == "dog"
    assert m.pet.barks == 3.14

    # Test Cat creation
    cat = Cat(pet_type="cat", meows=5)
    assert cat.pet_type == "cat"
    assert cat.meows == 5

    # Test Dog creation
    dog = Dog(pet_type="dog", barks=2.5)
    assert dog.pet_type == "dog"
    assert dog.barks == 2.5

    # Test Lizard creation
    lizard = Lizard(pet_type="reptile", scales=True)
    assert lizard.pet_type == "reptile"
    assert lizard.scales is True


def test_model_with_different_pets():
    # Test Model with Cat
    cat = Cat(pet_type="cat", meows=3)
    model_cat = Model(pet=cat, n=1)
    assert isinstance(model_cat.pet, Cat)
    assert model_cat.pet.pet_type == "cat"
    assert model_cat.n == 1


# def test_model_with_different_pets():
#     # Test Model with Cat
#     model_cat: Model = Model(pet=Cat(pet_type="cat", meows=3), n=1)
#     assert model_cat.pet.pet_type == "cat"
#     assert model_cat.n == 1

#     # Test Model with Dog
#     model_dog = Model(pet=Dog(pet_type="dog", barks=4.2), n=2)
#     assert model_dog.pet.pet_type == "dog"
#     assert model_dog.n == 2

#     # Test Model with Lizard
#     model_lizard = Model(pet=Lizard(pet_type="reptile", scales=True), n=3)
#     assert model_lizard.pet.pet_type == "reptile"
#     assert model_lizard.n == 3
