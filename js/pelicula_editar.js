console.log(location.search) // lee los argumentos pasados a este formulario
var id=location.search.substr(4)
console.log(id)
const { createApp } = Vue
createApp({
data() {
return {
id:0,
titulo:"",
descripcion:"",
anio:0,
duracion:0.0,
genero:"",
imagen:"",
url:'https://sebadimp.pythonanywhere.com/peliculas/'+id,
}
},
methods: {
fetchData(url) {
fetch(url)
.then(response => response.json())
.then(data => {

console.log(data)
this.id = data.id
this.titulo = data.titulo
this.descripcion = data.descripcion
this.anio = data.anio
this.duracion = data.duracion
this.genero = data.genero
this.imagen = data.imagen
})
.catch(err => {
console.error(err);
this.error=true
})
},
modificar() {
let pelicula = {
titulo:this.titulo,
descripcion:this.descripcion,
anio: this.anio,
duracion: this.duracion,
genero: this.genero,
imagen:this.imagen
}
var options = {
body: JSON.stringify(pelicula),
method: 'PUT',
headers: { 'Content-Type': 'application/json' },
redirect: 'follow'
}
fetch(this.url, options)
.then(function () {
alert("Registro modificado")
window.location.href = "../templates/peliculas.html";
})
.catch(err => {
console.error(err);
alert("Error al Modificar")
})
}
},
created() {
this.fetchData(this.url)
},
}).mount('#app')