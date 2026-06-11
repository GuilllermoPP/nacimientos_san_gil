from business_logic import *
import os

def clear_screen() -> None:
    """
    Limpia la consola de Windows.
    """

    os.system("cls")


def continue_program() -> bool:
    """
    Pregunta al usuario si desea
    realizar otra consulta.
    """

    while True:

        answer = input(
            "\n¿Desea realizar otra consulta?\n"
            "1. Sí\n"
            "0. No\n"
            "Seleccione una opción: "
        )

        if answer == "1":

            clear_screen()

            return True

        elif answer == "0":

            return False

        else:

            print(
                "\nOpción no válida."
            )

# ==========================================================
# FUNCIÓN PARA MOSTRAR EL MENÚ
# ==========================================================

def show_menu() -> None:
    """
    Muestra todas las opciones
    disponibles para el usuario.
    """

    clear_screen()

    print("\n")
    print("=" * 50)
    print("ANÁLISIS DE NACIDOS VIVOS")
    print("=" * 50)

    print("1. Peso promedio al nacer")
    print("2. Edad promedio de la madre")
    print("3. Edad promedio del padre")
    print("4. Tiempo promedio de gestación")

    print("\n--- Distribuciones ---")

    print("5. Nacimientos por sexo")
    print("6. Nacimientos por área")
    print("7. Nacimientos por EPS")
    print("8. Nacimientos por rango de edad materna")
    print("9. Nacimientos por grupo de edad gestacional")

    print("\n--- Consultas ---")

    print("10. EPS más frecuente")
    print("11. Tipo de parto más frecuente")
    print("12. Área más frecuente")

    print("\n--- Porcentajes ---")

    print("13. Porcentaje de cesáreas")
    print("14. Porcentaje de embarazos múltiples")

    print("\n--- Gráficas ---")

    print("15. Tiempo de gestación vs peso")
    print("16. Concepciones estimadas por semana")

    print("\n0. Salir")

    print("=" * 50)




# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

try:

    # Carga y valida el dataset utilizando
    # las funciones del business logic.
    borns = load_and_validate_dataset()

    print(
        "\nDataset cargado correctamente."
    )

    while True:

        show_menu()

        option = input(
            "\nSeleccione una opción: "
        )

        # ==================================================
        # OPCIÓN 1
        # ==================================================

        if option == "1":

            result = (
                calculate_average_birth_weight(
                    borns
                )
            )

            print(
                f"\nPeso promedio: "
                f"{result:.2f}"
            )

        # ==================================================
        # OPCIÓN 2
        # ==================================================

        elif option == "2":

            result = (
                calculate_average_mother_age(
                    borns
                )
            )

            print(
                f"\nEdad promedio de la madre: "
                f"{result:.2f}"
            )

        # ==================================================
        # OPCIÓN 3
        # ==================================================

        elif option == "3":

            result = (
                calculate_average_father_age(
                    borns
                )
            )

            print(
                f"\nEdad promedio del padre: "
                f"{result:.2f}"
            )

        # ==================================================
        # OPCIÓN 4
        # ==================================================

        elif option == "4":

            result = (
                calculate_average_gestation_time(
                    borns
                )
            )

            print(
                f"\nTiempo promedio de gestación: "
                f"{result:.2f}"
            )

        # ==================================================
        # OPCIÓN 5
        # ==================================================

        elif option == "5":

            print(
                "\nDistribución por sexo:"
            )

            print(
                count_births_by_sex(
                    borns
                )
            )

        # ==================================================
        # OPCIÓN 6
        # ==================================================

        elif option == "6":

            print(
                "\nDistribución por área:"
            )

            print(
                count_births_by_area(
                    borns
                )
            )

        # ==================================================
        # OPCIÓN 7
        # ==================================================

        elif option == "7":

            print(
                "\nDistribución por EPS:"
            )

            print(
                count_births_by_eps(
                    borns
                )
            )

        # ==================================================
        # OPCIÓN 8
        # ==================================================

        elif option == "8":

            print(
                "\nDistribución por rango de edad materna:"
            )

            print(
                count_births_by_maternal_age_group(
                    borns
                )
            )

        # ==================================================
        # OPCIÓN 9
        # ==================================================

        elif option == "9":

            print(
                "\nDistribución por grupo de edad gestacional:"
            )

            print(
                count_births_by_gestational_group(
                    borns
                )
            )

        # ==================================================
        # OPCIÓN 10
        # ==================================================

        elif option == "10":

            result = (
                find_most_common_eps(
                    borns
                )
            )

            print(
                f"\nEPS más frecuente: "
                f"{result}"
            )

        # ==================================================
        # OPCIÓN 11
        # ==================================================

        elif option == "11":

            result = (
                find_most_common_delivery_type(
                    borns
                )
            )

            print(
                f"\nTipo de parto más frecuente: "
                f"{result}"
            )

        # ==================================================
        # OPCIÓN 12
        # ==================================================

        elif option == "12":

            result = (
                find_most_common_area(
                    borns
                )
            )

            print(
                f"\nÁrea más frecuente: "
                f"{result}"
            )

        # ==================================================
        # OPCIÓN 13
        # ==================================================

        elif option == "13":

            result = (
                calculate_cesarean_percentage(
                    borns
                )
            )

            print(
                f"\nPorcentaje de cesáreas: "
                f"{result:.2f}%"
            )

        # ==================================================
        # OPCIÓN 14
        # ==================================================

        elif option == "14":

            result = (
                calculate_multiple_pregnancy_percentage(
                    borns
                )
            )

            print(
                f"\nPorcentaje de embarazos múltiples: "
                f"{result:.2f}%"
            )

        # ==================================================
        # OPCIÓN 15
        # ==================================================

        elif option == "15":

            print(
                "\nGenerando gráfica..."
            )

            generate_scatter_gestation_weight(
                borns
            )

        # ==================================================
        # OPCIÓN 16
        # ==================================================

        elif option == "16":

            print(
                "\nGenerando gráfica..."
            )

            generate_conception_pattern_graph(
                borns
            )

        # ==================================================
        # SALIR
        # ==================================================

        elif option == "0":

            print(
                "\nPrograma finalizado."
            )

            break

        # ==================================================
        # OPCIÓN INVÁLIDA
        # ==================================================

        else:

            print(
                "\nOpción no válida."
            )

            continue

        # ==================================================
        # CONTINUAR O FINALIZAR
        # ==================================================

        if not continue_program():

            print(
                "\nPrograma finalizado."
            )

            break

except Exception as error:

    print(
        f"\nError: {error}"
    )