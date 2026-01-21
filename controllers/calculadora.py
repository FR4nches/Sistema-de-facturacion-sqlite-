num1=input("Ingrese un numero:")
num2=input("Ingrese otro numero:")

print("Seleccione la operacion a arealizar")
print("1.SUMA")
print("2.RESTA")
print("3.DIVISION")
print("4.MULTIPLICACION")
opcion=input("Ingrese la opcion(1/2/3/4):")
if opcion == '1':
    print(num1,"+",num2,"=",float(num1)+float(num2))
elif opcion == '2':
    print(num1,"-",num2,"=",float(num1)-float(num2))
elif opcion == '3':
    print(num1,"/",num2,"=",float(num1)/float(num2))
elif opcion == '4':
    print(num1,"*",num2,"=",float(num1)*float(num2))
else:
    print("opcion invalida")
    
            
