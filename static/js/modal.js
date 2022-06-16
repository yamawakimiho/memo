const openModal = (options, id = null) => {
    $('#modal').modal('show');
    var modalTemplate = loadModalTemplates(options,id); 
    $("#modalTitle").html(modalTemplate.title);
    $("#modalDescription").html(modalTemplate.description);
    $("#modalButton").html(modalTemplate.button);
    return;
}

const loadModalTemplates = (options, id) => {
    var template = {};
        if(options === "addCard"){
            template.title = "Add new card";
            template.button = "<button type='button' class='loadingButtonSubmit btn btn-primary' onclick='addCard("+ id +")'>Create new card</button>";
            template.description = `
                <div class="form-group">
                    <label for="front">Front side of the new card (Question)</label>
                    <input type="text" class="form-control input-field" id="cardFront" aria-describedby="front">
                    <div  id="invalidCheckCardFront" class="invalid-feedback">
                    Please provide a question.
                    </div>
                    </div>
                    <div class="form-group">
                    <label for="back">Back side of the new card (Answer)</label>
                    <input type="text" class="form-control input-field" id="cardBack" aria-describedby="back">
                    <div  id="invalidCheckCardBack" class="invalid-feedback">
                    Please provide an answer.
                    </div>
                </div>`;
        }else if(options === "addDeck"){
            template.title = "Add new deck";
            template.button = "<button type='button' class='loadingButtonSubmit btn btn-primary' onclick='addDeck()'>Create new deck</button>";
            template.description = `
                <div class="form-group">
                    <label for="front">Name of the new deck (should contain at least 2 characters):</label>
                    <input type="text" class="form-control input-field" id="deckName" aria-describedby="front">
                    <div  id="invalidDeckName" class="invalid-feedback">
                    Please provide a name.
                    </div>
                    </div>
                    <div class="form-group">
                    <label for="back">Description</label>
                    <textarea type="text" class="form-control input-field" id="deckDescription" aria-describedby="back"></textarea>
                    <div  id="invalidDeckDescription" class="invalid-feedback">
                    Please provide a description.
                    </div>
                </div>`
        }else if(options === "deleteDeck"){
            template.title = "Delete deck confirmation";
            template.button = "<button type='button' class='loadingButtonSubmit btn btn-danger' onclick='deleteDeck("+ id +")'>Confirm Delete</button>";
            template.description = `
                <div class="form-group">
                    Are you sure you want to delete this deck?
                </div>`
        }else if(options === "updateCard"){
            cardInfo = getCardSelectorValue(id);

            template.title = "Update card";
            template.button = "<button type='button' class='loadingButtonSubmit btn btn-warning' onclick='updateCard("+ id +")'>Confirm Update</button>";
            template.description = `
                <div class="form-group">
                <label for="front">Front side of the new card (Question)</label>
                <input type="text" class="form-control input-field" value="${cardInfo.front}" id="cardFront" aria-describedby="front">
                <div  id="invalidCheckCardFront" class="invalid-feedback">
                Please provide a question.
                </div>
                </div>
                <div class="form-group">
                <label for="back">Back side of the new card (Answer)</label>
                <input type="text" class="form-control input-field" id="cardBack" value="${cardInfo.back}" aria-describedby="back">
                <div  id="invalidCheckCardBack" class="invalid-feedback">
                Please provide an answer.
                </div>
            </div>`;
        }else if(options === "historyCard"){
            template.title = "Answer History";
            template.button = "";

            let description = '<div class="form-group">'; 
            description += `<table class="table">
            <thead>
              <tr>
                <th scope="col">Answer</th>
                <th scope="col">Result</th>
                <th scope="col">Date</th>
              </tr>
            </thead>
            <tbody id="table_answer">`;
            description += '</tbody></table></div>';
            description += "<script>getAnswerHistory("+ id +")</script>";
            template.description = description;
        }
    return template;
}

returnIcon = (isCorrect) => {
    return (isCorrect) ? '✔️' : '❌';
};

isModalLoading = (isLoading) => {
    console.log($('.loadingButtonSubmit'));
      if(isLoading){
        $('#loadingButton').show();
        $('.loadingButtonSubmit').hide();
      }else{
        $('#loadingButton').hide();
        $('.loadingButtonSubmit').show();
      }
  }