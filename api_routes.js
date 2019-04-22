const controller = require('./controller')

module.exports = (app) => {

    app
        .get('/api/products', controller.all_products)
        .get('/api/products/:id', controller.show_product)
        .post('/api/products/', controller.create_product)
        .put('/api/products/:id', controller.update_product)
        .delete('/api/products/:id', controller.delete_product);
}