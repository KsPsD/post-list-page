function fetchPosts(page = 1) {
  $.ajax({
    url: `/api/posts/?page=${page}`,
    type: "GET",
    dataType: "json",
    success: function (data) {
      console.log(data);
      displayPosts(data.results);
      setupPagination(data.count, data.next, data.previous);
    },
    error: function (error) {
      console.log(error);
    },
  });
}

function displayPosts(posts) {
  let html = "";
  posts.forEach((post) => {
    html += `
                <div class="post">
                    <h2>${post.title}</h2>
                    <p>작성자: ${post.author}</p>
                    <p>최근 댓글: ${
                      post.latest_comment
                        ? post.latest_comment.content
                        : "댓글이 없습니다."
                    }</p>
                </div>
            `;
  });
  $("#posts-list").html(html);
}

function setupPagination(totalPosts, nextPage, prevPage) {
  let paginationHtml = "";
  if (prevPage) {
    let prevPageNumber = getPageNumber(prevPage);
    if (!prevPageNumber) {
      prevPageNumber = "1";
      prevPage +=
        (prevPage.includes("?") ? "&" : "?") + "page=" + prevPageNumber;
    }
    paginationHtml += `<a href="#" onclick="fetchPosts(${prevPageNumber})">이전</a>`;
  }
  // TODO: 현재 페이지를 계산하고 페이지 번호들을 렌더링할 로직을 추가합니다.
  if (nextPage) {
    paginationHtml += `<a href="#" onclick="fetchPosts(getPageNumber('${nextPage}'))">다음</a>`;
  }
  $("#pagination").html(paginationHtml);
}

function getPageNumber(url) {
  var urlParts = new URL(url);
  return urlParts.searchParams.get("page");
}

fetchPosts();
