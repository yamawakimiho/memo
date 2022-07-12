const paginationTemplate = (functionName,next,previous) => {
    previous = (!previous) ? 'disabled' : previous.split("?")[1];
    next = (!next) ? 'disabled' : next.split("?")[1];
  
    return ` <div class="col-md-12"><nav aria-label="page">
      <ul class="pagination hand">
        <li class="page-item ${previous}"><a class="page-link" onclick="${functionName}('${previous}')">Previous</a></li>
        <li class="page-item ${next}"><a class="page-link" onclick="${functionName}('${next}')" >Next</a></li>
      </ul>
    </nav></div>`
}