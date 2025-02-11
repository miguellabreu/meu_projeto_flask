module Square_mod
    implicit none
contains
    function getSquare(val) result(valSquared) bind(C, name="getSq")
        !DEC$ ATTRIBUTES DLLEXPORT :: getSquare
        use, intrinsic :: iso_fortran_env, only: RK => real64
        real(RK), intent(in) :: val
        real(RK)             :: valSquared
        valSquared = val ** 2
    end function getSquare
end module Square_mod