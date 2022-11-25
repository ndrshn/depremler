<template>
  <ul class="at-option-group">
    <li class="at-option-group__label">{{ props.label }}</li>
    <ul class="at-option-group__list">
      <slot></slot>
    </ul>
  </ul>
</template>

<script setup>
const props = defineProps({
  label: {
    type: String,
    required: true,
  },
});
</script>

<style>
.at-option-group {
  padding: 0;
}

.at-option-group__label {
  display: inline-block;
  max-width: 100%;
  text-overflow: ellipsis;
  word-wrap: normal;
  width: 100%;
  padding: 8px;
  color: #bfbfbf;
  font-size: 12px;
  line-height: 1;
  white-space: nowrap;
  overflow: hidden;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;
  cursor: initial;
}

.at-option-group__list {
  padding: 0;
}
</style>
