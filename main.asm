reset:
  lda #$44
  sta $1222

loop:
  nop

  jmp loop

  .org $fffc
  .word reset
  .word $0000