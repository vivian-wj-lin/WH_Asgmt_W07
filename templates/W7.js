//搜尋name
const searchButton = document.querySelector(".searchButton")
searchButton.addEventListener("click", function(){
  const username = document.querySelector(".currentName").value

  fetch(`/api/member?username=${username}`)
    .then((response) => {
      return response.json()
    })
    .then((Data) => {
      // console.log("Data")//{data: {…}}

      const data = Data.data
      // console.log(data)//{id: 2, name: 'hello', username: 'test2'}

      const name = data.name
      const username = data.username
      const details = document.querySelector(".search")
      const newDiv = document.createElement("div")
      newDiv.textContent = `${name} (${username})`
      details.appendChild(newDiv)
    })
})


//更新name
const updateButton = document.querySelector(".updateButton")
updateButton.addEventListener("click", function(){
  const newUsername = document.querySelector(".typeNewUsername").value

  fetch('/api/member', {
    method: 'PATCH',
    body: JSON.stringify({ name: newUsername }),
    headers: { "content-type": "application/json"},
  }).then(() => {
    document.querySelector(".updateDone").textContent = "更新成功"
    const hello = document.querySelector("span")
    hello.textContent = `${newUsername}`
  })
})


