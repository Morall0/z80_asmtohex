      LD BC, 127
      LD A, 0; r <- 0
      LD (1000H), A 
      ; RELOCALIZACION CON ESPACIOS
      LD B, 0; BC <- n (tamamaño del bloaque)
      LD A, (1001H)
      LD C, A
      LD HL, 1001H; HL <- o[n-1]
      ADD HL, BC
      LD DE, 7FFFH; DE <- d[m-1] de la memoria

      LDDR
      INC DE; DE <- d[0]

      ; BUSQUEDA DE LOS ESPACIOS
      LD A, (1001H); BC <- n (tamaño del bloque) ; TODO CAMBIAR EL TAMANO DEL BLOQUE
      LD C, A
eti2:
      LD H, D; HL <- DE
      LD L, E;
      LD A, 0; A <- 0
      CPIR
      LD A, C
      CP 0
      JP Z, eti1;
      DEC HL

      ; ELIMINACION DEL ESPACIO (RECORRIDO) 
      LD A, L
      SUB E
      LD C, A
      EX DE, HL
      ADD HL, BC
      DEC L
      ;LD A, 0 No es necesario cargar A con 0
      LDDR
      INC DE; DE <- d[0]
      INC HL
      LD A, E; Encontrando cantidad de espacios
      SUB L
      LD H, A; Respaldando cantidad de espacios quitados en H
      LD A, (1001H); A <- n
      SUB H; Restandole al tamaño los espacios quitados
      LD (1001H), A; Cambiando en la memoria el tamaño del bloque
      LD C, A; BC <- nuevo n
      JP eti2 
eti1:
      HALT

eti0: LD A, (1000)
