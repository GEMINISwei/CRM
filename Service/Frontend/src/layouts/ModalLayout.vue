<script lang="ts" setup>
import { reactive, onMounted, watch } from 'vue'
import { Modal } from 'bootstrap'
import { statusFlag, setStatusFlag } from '@/composables/globalUse'

const htmlElems = reactive<any>({
  modal: null
})

onMounted(() => {
  let modalElem = document.querySelector("#system-modal") as HTMLElement

  htmlElems.modal = new Modal(modalElem)
  modalElem.addEventListener('hide.bs.modal', () => {
    setStatusFlag('modalShow', false)
  })
})

watch(() => statusFlag.modalShow, (status: boolean) => {
  if (status) {
    htmlElems.modal.show()
  } else {
    htmlElems.modal.hide()
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
</template>
