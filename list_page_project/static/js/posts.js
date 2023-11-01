const postManager = {
  fetchPosts: function (page = 1, searchQuery = "") {
    let url = `/api/posts/?page=${page}`;
    if (searchQuery) {
      url += `&search=${encodeURIComponent(searchQuery)}`;
    }

    $.ajax({
      url: url,
      type: "GET",
      dataType: "json",
      success: (data) => {
        this.displayPosts(data.results);
        this.setupPagination(
          data.count,
          data.links.next,
          data.links.previous,
          page,
          data.pageSize
        );
      },
      error: () => {
        alert("데이터를 가져오는데 문제가 발생했습니다.");
      },
    });
  },

  searchPosts: function () {
    const query = $("#search-field").val();
    this.fetchPosts(1, query);
  },

  resetSearch: function () {
    $("#search-field").val("");
    this.fetchPosts();
  },

  displayPosts: function (posts) {
    const MAX_COMMENT_LENGTH = 50;
    let html = "";
    posts.forEach((post) => {
      let commentText = "댓글이 없습니다.";
      if (post.latest_comment) {
        commentText = post.latest_comment.content;
        if (commentText.length > MAX_COMMENT_LENGTH) {
          commentText = commentText.substring(0, MAX_COMMENT_LENGTH) + " ...";
        }
      }

      html += `
        <div class="post">
          <h2><a href="/posts/${post.id}/">${post.title}</a></h2>
          <p>작성자: ${post.author.username}</p>
          <p>최근 댓글: ${commentText}</p>
        </div>
      `;
    });
    $("#posts-list").html(html);
  },

  setupPagination: function (
    totalPosts,
    nextPage,
    prevPage,
    currentPage,
    pageSize
  ) {
    let paginationHtml = "";
    const totalPages = Math.ceil(totalPosts / pageSize);

    if (prevPage) {
      paginationHtml += `<a href="#" class="page-link" data-page="${
        currentPage - 1
      }">이전</a> <t>`;
    }

    if (nextPage) {
      paginationHtml += `<a href="#" class="page-link" data-page="${
        currentPage + 1
      }">다음</a> <t>`;
    }

    paginationHtml += `<div> Page Navigator:`;
    for (let i = 1; i <= totalPages; i++) {
      paginationHtml += `<a href="#" class="page-link" data-page="${i}">${i}</a> <t>`;
    }
    paginationHtml += `</div>`;
    paginationHtml += `<t> <div>현재 페이지: ${currentPage}</div>`;
    $("#pagination").html(paginationHtml);

    $(".page-link").click((event) => {
      event.preventDefault();
      const page = $(event.target).data("page");
      this.fetchPosts(page);
    });
  },

  init: function () {
    this.fetchPosts();
  },
};

$(document).ready(function () {
  postManager.init();

  $("#search-button").click(function () {
    postManager.searchPosts();
  });

  $("#search-field").on("keypress", function (e) {
    if (e.which === 13) {
      postManager.searchPosts();
    }
  });

  $("#reset-button").click(function () {
    postManager.resetSearch();
  });
});
