#include <stdio.h>
#include <stdbool.h> //Esto para trabajar con booleans

int main(){
    //La funcion "main" es necesaria

    //VARIABLES:
    //-Los INTERGER no pueden guardar decimales.
    int age = 16;
    int year = 2025;
    int fruits = 2;

    printf("You are %d years old \n", age);
    printf("The year is %d \n", year);
    printf("Your have ordered %d fruits \n \n", fruits);

    //-Los FLOAT pueden guardar decimales.
    float gpa = 2.5;
    float price = 19.99;

    printf("Your gpa is %.1f \n", gpa); //.1 hace que solo se printeen los 2 primers decimales, si no pondria 2.500000...
    printf("This costs %.2f$\n", price);

    //-Digamos que necesitas decimales MUY precisos:
    //Aquí entran los DOUBLE

    double pi = 3.14159265358979;

    printf("Pi is equal to %.14lf\n", pi);//lf significa long float, el default de c es ".6"

    //-Characters:

    char grade = 'A'; // si o si hay que usar el '

    printf("Your grade was %c\n", grade);

    //NO HAY STRINGS PERO HAY WUE HACER ETO KJSDHFKJSDFK:
    //Un array, muchos characters en una lista basicamente fsdkgjhfdgjksnghk

    char name[] = "Lauret"; // si o si hay que usar las ""

    printf("My name is %s\n", name); //s = string

    //Como no, los booleans:

    bool isHeFriendly = true;

    if(isHeFriendly){
        printf("He is friendly :D");
    }
    else{
        printf("He is not friendly, RUNNNN");
    }

    return 0; //se suele usar return pq se espera que devuelva algo ya tu sabe'
}