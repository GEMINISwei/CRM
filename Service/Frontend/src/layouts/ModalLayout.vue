<script lang="ts" setup>
import { reactive, onMounted, watch } from 'vue'
import { Modal } from 'bootstrap'
import { statusFlag, setStatusFlag } from '@/composables/globalUse'

const htmlElems = reactive<any>({
  modal: null,
  modal2: null,
})

onMounted(() => {
  let modalElem = document.querySelector("#system-modal") as HTMLElement

  htmlElems.modal = new Modal(modalElem)
  modalElem.addEventListener('hide.bs.modal', () => {
    setStatusFlag('modalShow', false)
  })

  let modalElem2 = document.querySelector("#system-modal-2") as HTMLElement

  htmlElems.modal2 = new Modal(modalElem2)
  modalElem2.addEventListener('hide.bs.modal', () => {
    setStatusFlag('modalShow2', false)
  })
})

watch(() => statusFlag.modalShow, (status: boolean) => {
  if (status) {
    htmlElems.modal.show()
  } else {
    htmlElems.modal.hide()
  }
})
watch(() => statusFlag.modalShow2, (status: boolean) => {
  if (status) {
    htmlElems.modal2.show()
  } else {
    htmlElems.modal2.hide()
  }
})
</script>

<template>
  <!-- <div id="system-modal" class="modal modal-lg fade" data-bs-backdrop="static"> -->
  <div id="system-modal" class="modal modal-lg fade">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <div id="modal-header" class="w-100 text-center"></div>
          <!-- 暫時不開放 Close Btn, 方便頁面做狀態控管 -->
          <button class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body d-flex justify-content-center mt-4">
          <div id="modal-body" class="w-75"></div>
        </div>
        <!-- <div class="modal-footer d-flex justify-content-center">
          <div id="modal-footer"></div>
        </div> -->
      </div>
    </div>
  </div>

  <div id="system-modal-2" class="modal modal-lg fade">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <div id="modal-header-2" class="w-100 text-center"></div>
          <!-- 暫時不開放 Close Btn, 方便頁面做狀態控管 -->
          <button class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body d-flex justify-content-center mt-4">
          <div id="modal-body-2" class="w-75"></div>
        </div>
        <!-- <div class="modal-footer d-flex justify-content-center">
          <div id="modal-footer"></div>
        </div> -->
      </div>
    </div>
  </div>
</template>
