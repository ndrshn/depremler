<template>
  <transition name="fade">
    <span class="os-tag" :class="[colorClass]" :style="colorStyle">
      <span class="os-tag__text">
        <slot></slot>
      </span>
      <i v-if="props.closable" class="icon icon-x os-tag__close" @click="closeAction"></i>
    </span>
  </transition>
</template>

<script setup>
import { computed } from "vue";

const colorArr = ["default", "primary", "success", "error", "warning", "info"];

const emit = defineEmits(["on-close"]);
const props = defineProps({
  name: {
    type: [String, Number],
  },
  color: {
    type: String,
    default: "default",
  },
  closable: {
    type: Boolean,
    default: false,
  },
});

const colorClass = computed(() => {
  return colorArr.indexOf(props.color) > -1 ? `os-tag--${props.color}` : "";
});

const colorStyle = computed(() => {
  if (colorArr.indexOf(props.color) > -1) return "";
  return {
    borderColor: props.color,
    backgroundColor: props.color,
  };
});

const closeAction = (evt) => {
  if (typeof props.name === "undefined") {
    emit("on-close", evt);
  } else {
    emit("on-close", evt, props.name);
  }
};
</script>

<style>
.os-tag {
  display: inline-block;
  padding: 1px 8px;
  color: #fff;
  font-size: 0;
  line-height: 1.5;
  text-align: center;
  white-space: nowrap;
  border: 1px solid #dfdfdf;
  border-radius: 4px;
  outline: 0;
  color: #3f536e;
  border-color: #dfdfdf;
  background-color: #f7f7f7;
}

.os-tag__text {
  font-size: 12px;
}

.os-tag__close {
  font-size: 10px;
  padding-left: 4px;
  margin: 0;
  cursor: pointer;
}

.os-tag__close:hover {
  color: #79879a;
}

.os-tag--default {
  color: #3f536e;
  border-color: #dfdfdf;
  background-color: #f7f7f7;
}

.os-tag--primary {
  color: #fff;
  border-color: #6190e8;
  background-color: #6190e8;
}

.os-tag--success {
  color: #fff;
  border-color: #13ce66;
  background-color: #13ce66;
}

.os-tag--error {
  color: #fff;
  border-color: #ff4949;
  background-color: #ff4949;
}

.os-tag--warning {
  color: #fff;
  border-color: #ffc82c;
  background-color: #ffc82c;
}

.os-tag--info {
  color: #096dd9;
  border-color: #91d5ff;
  background-color: #e6f7ff;
}
</style>
