from typing import Dict
from hexagon.utils.monad import IdentityMonad
from functools import partial
from InquirerPy import inquirer
import requests


def __id_name_to_choice(id_name: Dict) -> Dict:
    return {"name": id_name["name"], "value": id_name["id"]}


map_id_name_to_choice = partial(map, __id_name_to_choice)


def scaffold_springboot():
    initializr_data = requests.get("https://start.spring.io/metadata/client").json()

    project_type = inquirer.select(
        message="¿Qué tipo de proyecto querés armar?",
        choices=IdentityMonad(initializr_data["type"]["values"])
        .bind(partial(filter, lambda type: type["tags"]["format"] == "project"))
        .bind(map_id_name_to_choice)
        .value,
        default=initializr_data["type"]["default"],
    ).execute()

    language = inquirer.select(
        message="¿Qué lenguaje vas a usar?",
        choices=IdentityMonad(initializr_data["language"]["values"])
        .bind(map_id_name_to_choice)
        .value,
        default=initializr_data["language"]["default"],
    ).execute()

    springboot_version = inquirer.select(
        message="¿Qué versión de Spring Boot?",
        choices=IdentityMonad(initializr_data["bootVersion"]["values"])
        .bind(map_id_name_to_choice)
        .value,
        default=initializr_data["bootVersion"]["default"],
    ).execute()

    print(project_type)
    print(language)
    print(springboot_version)
