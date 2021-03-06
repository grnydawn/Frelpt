!
! This file is released under terms of BSD license
! See LICENSE file for more information
!

MODULE mo_column_extra
  USE mo_column, ONLY: ty_column, compute_column
  IMPLICIT NONE

CONTAINS

  SUBROUTINE compute_one(nz, q, t)
    IMPLICIT NONE

    INTEGER, INTENT(IN)   :: nz   ! Size of the array field
    REAL, INTENT(INOUT)   :: t(:) ! Field declared as one column only
    REAL, INTENT(INOUT)   :: q(:) ! Field declared as one column only
    TYPE(ty_column)       :: column
    integer i


    !$claw parallelize forward
    CALL column%compute_column(nz, q, t)

    !!!! TEST YKS
    !q = 0

    do i=2, nz
       q(i) = q(i-1) + t(i)
    end do
 
  END SUBROUTINE compute_one

END MODULE mo_column_extra
