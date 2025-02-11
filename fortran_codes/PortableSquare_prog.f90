program Square_prog
    use, intrinsic :: iso_fortran_env, only: RK => real64
    use Square_mod, only: getSquare
    implicit none
    real(RK) :: val = 100._RK
    interface
    function getSq(val) result(valSquared)
        !DEC$ ATTRIBUTES DLLIMPORT, DECORATE, ALIAS: 'getSq' :: getSq
        use, intrinsic :: iso_fortran_env, only: RK => real64
        real(RK), intent(in) :: val
        real(RK)             :: valSquared
    end function getSq
    end interface
    write(*,"(*(g0.13,:,' '))") "getSquare(", val, ") =", getSquare(val)
    write(*,"(*(g0.13,:,' '))") "    getSq(", val, ") =", getSq(val)
end program Square_prog