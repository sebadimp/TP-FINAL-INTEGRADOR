const { createApp } = Vue
createApp({
data() {
return {
peliculas:[],
//url:'http://localhost:5000/peliculas',
// si el backend esta corriendo local usar localhost 5000(si no lo subieron a pythonanywhere)
url:'https://sebadimp.pythonanywhere.com/peliculas', // si ya lo subieron a pythonanywhere
error:false,
cargando:true,
/*atributos para el guardar los valores del formulario */
id:0,
titulo:"",
descripcion:"",
anio:0,
duracion:0.0,
genero:"",
imagen:""
}
},
methods: {
fetchData(url) {
fetch(url)
.then(response => response.json())
.then(data => {
this.peliculas = data;
this.cargando=false
})
.catch(err => {
console.error(err);
this.error=true
})
},
eliminar(pelicula) {
const url = this.url+'/' + pelicula;
var options = {
method: 'DELETE',
}
fetch(url, options)
.then(res => res.json()) // or res.json()
.then(res => {
location.reload();
})
},
grabar(){
let pelicula = {
titulo:this.titulo,
descripcion:this.descripcion,
anio: this.anio,
duracion: this.duracion,
genero: this.genero,
imagen:this.imagen
}
var options = {
body:JSON.stringify(pelicula),
method: 'POST',
headers: { 'Content-Type': 'application/json' },
redirect: 'follow'
}
fetch(this.url, options)
.then(function () {
alert("Registro guardado")
window.location.href = "../TP-FINAL-INTEGRADOR/templates/index.html";
})
.catch(err => {
console.error(err);
alert("Error al guardar")
})
}
},
created() {
this.fetchData(this.url)
},
}).mount('#app')