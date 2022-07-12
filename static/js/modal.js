const openModal = (options, id = null) => {
    $('#modal').modal('show');
    let modalTemplate = loadModalTemplates(options,id); 
    $("#modalTitle").html(modalTemplate.title);
    $("#modalDescription").html(modalTemplate.description);
    $("#modalButton").html(modalTemplate.button);
    return;
}

const loadModalTemplates = (options, id) => {
    let template = {};
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
        }else if(options === "getPresetDeckDetails"){
            let presetDeck = presetDeckData.results[id];
            let cardsDetails = "";

            for(let card in presetDeck.preset_cards){
                cardsDetails += 
                    `<tr>
                        <td>${presetDeck.preset_cards[card].front}</td>
                        <td>${presetDeck.preset_cards[card].back}</td>
                    </tr>`;
            }

            template.title = `Deck name: ${presetDeck.name}`
            template.description = `
                <div class="form-group">
                <p><b>Created at:</b> ${presetDeck.created_at} - <b>Total Cards:</b> ${presetDeck.preset_cards.length}</p>
                <p><b>Description of this deck:</b> ${presetDeck.description}</p>
                <table class="table">
                <thead>
                  <tr>
                    <th scope="col">Front</th>
                    <th scope="col">Back</th>
                  </tr>
                </thead>
                <tbody>
                    ${cardsDetails}
                </tbody>
                </table>
                </div>`;
        }

    return template;
}

returnIcon = (isCorrect) => {
    return (isCorrect) ? '✔️' : '❌';
};

isModalLoading = (isLoading) => {
      if(isLoading){
        $('#loadingButton').show();
        $('.loadingButtonSubmit').hide();
      }else{
        $('#loadingButton').hide();
        $('.loadingButtonSubmit').show();
      }
  }