const recipe = {
    title: 'Title',
    content: 'content kurwo'
}

function getRecipeTitle() {
    const element = document.getElementById('receipe-title')
    element.innerHTML = recipe.title
}

function getRecipeContent() {
    return recipe.content;
}