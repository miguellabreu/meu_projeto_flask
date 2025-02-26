
    subroutine write_xy_em_memoria(n, x_array, y_array) bind(c, name='write_xy_em_memoria')
        
        use, intrinsic :: iso_c_binding
        implicit none
        integer(c_int), value, intent(in) :: n
        real(c_float), intent(out) :: x_array(n)  ! Array de saída para x
        real(c_float), intent(out) :: y_array(n)  ! Array de saída para y
        integer :: i
        
        ! Gerar valores
        do i = 1, n
            x_array(i) = real(i, c_float) * 0.01_c_float
            y_array(i) = sin(x_array(i))
        end do
        
        print *, "Arrays gerados com sucesso. Total de pontos:", n
        
    end subroutine write_xy_em_memoria
    

