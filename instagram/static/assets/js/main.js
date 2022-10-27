function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
  
  function getAllPosts(url) {
    fetch(url, {
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      }
    })
    .then(response => response.json())
    .then(data => {
      const postList = document.getElementById("todoList");
      postList.innerHTML = "";
  
      (data.context).forEach(post => {
        const postHTMLElement = `
          <li>
            <p>Task: ${post.task}</p>
            <p>Completed?: ${post.completed}</p>
          </li>`
          postList.innerHTML += postHTMLElement;
      });
    });
  }