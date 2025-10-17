#include <stdio.h>

int main(){

    //-Format especifiers = Son un token que comienza con un simbolo %, seguido de un especificador de data,
    //                      Siendo este una letra y modificadores opcionales.
    //                      Controlan como la data se muestra o interpreta.

    int age = 16;
    float price = 9.99;
    double pi = 3.1415826565;
    char currency = '$';
    char name[] = "Lauret";

    printf("%5d \n", age); //el 4 indica 4 caracteres MINIMO Y MAXIMO.
    printf("%-5d \n", age); // puede ser negativo.
    printf("%05d \n", age); // o que los espacios sean ceros.
    printf("%+d \n", age); // los números positivos tendrán el simbolo, negativos TOOOOOOOOOOOOOO.

    printf("%.2f \n", price);
    printf("%.10lf \n", pi); // el "." te dirá cuantos decimales usar.

    printf("%c \n", currency);
    printf("%s \n", name);

}