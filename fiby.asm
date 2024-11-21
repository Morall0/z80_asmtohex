    LD A, (3000H); Se lee n (el término a calcular [0, 46])
    LD HL, 0; Se establece la suma de términos en cero
    LD (3002H), HL
    LD (3004H), HL; Se limpian las localidades donde se plasma el resultado
    CALL fib
    HALT

fib:
    CP 1
    JP Z, c_base_1; Caso base para F(1) = 1
    CP 0
    JP Z, dr1; Caso base para F(0) = 0
    DEC A; Se decrementa n para calcular F(n-1)
    PUSH AF; Se guarda n-1 en la pila
    CALL fib; Se llama a recursión para F(n-1)
    POP AF; Se extrae n-1 de la pila
    DEC A; Se decrementa a n-2 para hacer el cálculo de n-2
    CALL fib; Se llama a recursión para F(n-2)
dr1:
    RET

c_base_1:
    LD DE, 1; Simulación de incremento que permite el uso del Carry
    ADD HL, DE; Se incrementa la parte baja del resultado
    LD (3004H), HL; Se almacena la parte baja del resultado
    LD HL, (3002H); Se carga la parte alta del resultado
    
    ; Se limpia DE para que se pueda considerar el Carry en la suma del 
    ; resultado en su parte alta. Al final se asegura que el Carry se 
    ; halle apagado
    LD DE, 0
    ADC HL, DE
    SCF
    CCF
    
    ; Se guarda la parte alta en la memoria y se carga la baja en HL
    LD (3002H), HL
    LD HL, (3004H)
    JP dr1
