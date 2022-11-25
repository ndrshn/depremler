<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <li
    v-show="!hidden"
    ref="option"
    class="os-select__option"
    :class="[
      disabled ? 'os-select__option--disabled' : '',
      selected ? 'os-select__option--selected' : '',
      isFocus ? 'os-select__option--focus' : '',
    ]"
    @click.stop="doSelect"
    @mouseout.stop="blur"
  >
    <slot>{{ showLabel }}</slot>
  </li>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, getCurrentInstance } from "vue";

const props = defineProps({
  value: {
    type: [String, Number],
    required: true,
  },
  label: {
    type: [String, Number],
    required: true,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
});

const parent = getCurrentInstance().parent.parent.parent;
const selected = ref(false);
const option = ref();
const isFocus = ref(false);
const hidden = ref(false);
const searchLabel = ref("");
const showLabel = computed(() => {
  return props.label ? props.label : props.value;
});

const doSelect = () => {
  if (props.disabled) return false;
  parent.exposed.onSelectSelected(props.value);
};

const blur = () => {
  isFocus.value = false;
};

onMounted(() => {
  searchLabel.value = option.value.innerHTML;
});

onBeforeUnmount(() => {
  if (parent.exposeProxy.options && parent.exposeProxy.options.length > 0) {
    parent.exposeProxy.options.forEach((option, idx) => {
      if (option._instance === this) {
        parent.exposeProxy.onOptionDestroy(idx);
      }
    });
  }
});
</script>

<style></style>
