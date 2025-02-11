#if defined (BUILD_DLL)
MODULE DLL_FUNCTIONS
    USE, INTRINSIC :: ISO_C_BINDING
    IMPLICIT NONE
END MODULE DLL_FUNCTIONS
#endif

SUBROUTINE minha_funcao(x, resultado) bind(C,name="minha_funcao")
    !DEC$ ATTRIBUTES DLLEXPORT :: minha_funcao 
    !DEC$ ATTRIBUTES REFERENCE :: resultado    ! resultado é passado por referência
    !DEC$ ATTRIBUTES VALUE :: x                ! x é passado por valor
    USE ISO_C_BINDING
    IMPLICIT NONE
    REAL(C_DOUBLE), VALUE, INTENT(IN) :: x
    REAL(C_DOUBLE), INTENT(OUT) :: resultado
    resultado = x * 2.0
END SUBROUTINE minha_funcao

#if !defined (BUILD_DLL)
PROGRAM main
    USE ISO_C_BINDING
    IMPLICIT NONE
    
    REAL(C_DOUBLE) :: x = 5.0
    REAL(C_DOUBLE) :: resultado
    
    CALL minha_funcao(x, resultado)
    PRINT *, "Resultado:", resultado
END PROGRAM
#endif

! referencia . ponteiro
! dumpin em memoria

! 
! 
! 1. Passagem por Valor (entrada):
!    - utiliza ctypes.c_double
!    - Valor é copiado para Fortran
!    - Alterações em Fortran não são refletidas em Python

! 2. Passagem por Referência (saida):
!    - utiliza POINTER(ctypes.c_double)
!    - Memória é compartilhada com Fortran
!    - Alterações em Fortran são refletidas em Python

! 
