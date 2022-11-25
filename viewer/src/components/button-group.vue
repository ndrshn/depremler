<template>
  <div class="os-btn-group" :class="[props.size ? `os-btn-group--${props.size}` : '']">
    <slot></slot>
  </div>
</template>

<script setup>
const props = defineProps({
  size: String,
  gap: {
    type: Number,
    default: -1,
  },
});
</script>

<style>
.os-btn-group {
  font-size: 0;
  display: inline-block;
}

.os-btn-group .os-btn {
  border-radius: 0;
}

.os-btn-group .os-btn:not(:last-child) {
  margin-right: -1px;
}

.os-btn-group .os-btn:first-child {
  border-radius: 4px 0 0 4px;
}

.os-btn-group .os-btn:last-child {
  border-radius: 0 4px 4px 0;
}
</style>
