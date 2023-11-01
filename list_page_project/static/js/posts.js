function fetchPosts(page = 1, searchQuery = "") {
  let url = `/api/posts/?page=${page}${
    searchQuery && `&search=${encodeURIComponent(searchQuery)}`
  }`;

  $.ajax({
    url: url,
    type: "GET",
    dataType: "json",
    success: function (data) {
      displayPosts(data.results);
      setupPagination(
        data.count,
        data.links.next,
        data.links.previous,
        page,
        data.pageSize
      );
    },
    error: function (error) {
      alert("데이터를 가져오는데 문제가 발생했습니다.");
    },
  });
}

function searchPosts() {
  const query = $("#search-field").val();
  fetchPosts(1, query);
}

function resetSearch() {
  $("#search-field").val("");
  fetchPosts();
}

function displayPosts(posts) {
  let html = "";
  posts.forEach((post) => {
    authorUsername = post.author.username;
    html += `
                <div class="post">
                    <h2><a href="/posts/${post.id}/">${post.title}</a></h2>
                    <p>작성자: ${post.author.username}</p>
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

function setupPagination(
  totalPosts,
  nextPage,
  prevPage,
  currentPage,
  pageSize
) {
  let paginationHtml = "";
  const totalPages = Math.ceil(totalPosts / pageSize);
  if (prevPage) {
    paginationHtml += `<a href="#" onclick="fetchPosts(${
      currentPage - 1
    })">이전</a> <t>`;
  }

  if (nextPage) {
    paginationHtml += `<a href="#" onclick="fetchPosts(${
      currentPage + 1
    })">다음</a> <t>`;
  }
  paginationHtml += `<div> Page Navigator:`;
  for (let i = 1; i <= totalPages; i++) {
    paginationHtml += `<a href="#" onclick="fetchPosts(${i})">${i}</a> <t>`;
  }
  paginationHtml += `</div>`;
  paginationHtml += `<t> <div>현재 페이지: ${currentPage}</div>`;
  $("#pagination").html(paginationHtml);
}

fetchPosts();
