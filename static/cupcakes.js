const BASE_URL = "http://localhost:5000/api";

$('.delete-cupcake').click(deleteCupcake)

async function deleteCupcake() {
  const id = $(this).data('id')
  await axios.delete(`/api/cupcakes/${id}`)
  $(this).parent().remove()
}

$('.add-cupcake-form').click(newCupcake)

async function newCupcake() {

  let flavor = $("#form-flavor").val();
  let rating = $("#form-rating").val();
  let size = $("#form-size").val();
  let image = $("#form-image").val();
  
  const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image
  });
  
  let newCupcake = newCupcakeResponse.data.cupcake
  $("#cupcakes-list").append(newCupcake);
  $("#new-cupcake-form").trigger("reset");
}



