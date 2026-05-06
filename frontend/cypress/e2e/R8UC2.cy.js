let email;
let uid;
describe('Use case R8UC2', () => {
    before(() => {
        cy.fixture('user.json').then((user) => {
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/users/create',
                form: true,
                body: user
            }).then((response) => {
                email = user.email;
                uid = response.body._id.$oid;
                cy.fixture('task.json').then((task) => {
                    cy.request({
                        method: 'POST',
                        url: 'http://localhost:5000/tasks/create',
                        form: true,
                        body: {
                            title: task.title,
                            description: task.description,
                            url: task.url,
                            userid: uid,
                            todos: task.todos[0]
                        }
                    }).then((response) => {
                        cy.visit('http://localhost:3000');
                        cy.get('#email').type(email);
                        cy.get('form').submit();

                        // cy.contains(task.title).click();
                    });
                });
            });

        });
    });

    after(() => {
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`,
        }).then((response) => {
            expect(response.body.success).to.be.true;
        });
    });

    it('The user enters a description of a todo item and creates it', () => {
        cy.get('.inline-form > [type="text"]').type('todo test');
    });
    // it('marks an active todo as done and crosses out its text', () => {
    //     cy.contains('.todo-item', 'todo test')
    //         .as('todoTestItem');

    //     cy.get('@todoTestItem')
    //         .find('span.checker').click();

    //     cy.get('@todoTestItem')
    //         .find('span.checker')
    //         .should('have.class', 'checked');

    //     cy.get('@todoTestItem')
    //         .find("span.editable")
    //         .should('have.css', 'text-decoration-line', 'line-through');
    // });

    // it('mark done todos as active and text is no longer crossed out', () => {
    //     cy.contains('.todo-item', 'todo test')
    //         .as('todoTestItem');

    //     cy.get('@todoTestItem')
    //         .find('span.checker').click();

    //     cy.get('@todoTestItem')
    //         .find('span.checker')
    //         .should('not.have.class', 'checked');

    //     cy.get('@todoTestItem')
    //         .find("span.editable")
    //         .should('have.css', 'text-decoration-line', 'none');

    // });

});
