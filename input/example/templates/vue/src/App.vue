<template>
    <div id="app">
        @@add-component-in-template@@
        <user-view />
    </div>
</template>

<script>
@@add-imports@@
import User from "@/views/User.vue"

export default {
    name: 'app',
    components:{
        'user-view': User,
@@add-component-in-class@@
    }
}
</script>
