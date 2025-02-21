function all_total_price()
{


    const l =document.getElementsByName("price")
    let sum = 0;
    for (let i = 0; i < l.length; i++) {
        sum += parseFloat(l[i].value);
    }
    document.getElementById("all_total_price").innerText = sum.toFixed(2);
}
function createTableRow(n, category_id, category, purchase_price, quantity, sub_element_quantity, sub_element_quantity_default) {
    const tr = document.createElement('tr');

    tr.innerHTML = `
        <td>
            <select name="items-${n}-category" class="form-control" id="id_items-${n}-category" 
                aria-describedby="id_items-${n}-category_helptext">
                <option selected value="${category_id}">${category}</option>
            </select>
        </td>
        <td>
            <input type="number" name="items-${n}-purchase_price" class="form-control" 
                id="id_items-${n}-purchase_price" value="${purchase_price}" step="0.01" 
                placeholder="أدخل سعر الشراء">
        </td>
        <td>
            <input type="number" name="items-${n}-quantity" class="form-control" 
                id="id_items-${n}-quantity" value="${quantity}" min="0" 
                placeholder="أدخل الكمية">
        </td>
        <td>
            <input type="number" name="items-${n}-sub_element_quantity" class="form-control" 
                id="id_items-${n}-sub_element_quantity" value="${sub_element_quantity}" min="0" 
                placeholder="أدخل الكمية الفرعية">
        </td>
        <input type="hidden" name="items-${n}-invoice" id="id_items-${n}-invoice">
        <input type="hidden" name="items-${n}-id" id="id_items-${n}-id">
        <input type="hidden" name="items-${n}-category_sub_element_quantity" 
            id="id_items-${n}-category_sub_element_quantity" value="${sub_element_quantity_default}" readonly>
        <td>
            <div class="mb-3">
                <input type="number" name="price" class="form-control numberinput" 
                    id="id_items-${n}-DELETE_total_price" value="1.00" step="0.01" readonly disabled 
                    placeholder="أدخل سعر الشراء">
            </div>
        </td>
        <td>
            <input type="checkbox" name="items-${n}-DELETE" id="id_items-${n}-DELETE">
        </td>
    `;

    return tr;
}

function addTableRow(event) {
    if (event) event.preventDefault();

    try {
        const n = Number(document.getElementById("id_items-TOTAL_FORMS").value);
        const category_id = Number(document.getElementById("category_id").value);
        const category = document.getElementById("category").value;
        const purchase_price = Number(document.getElementById("pruchase_price").value);
        const quantity = Number(document.getElementById("quantity").value);
        const sub_element_quantity = Number(document.getElementById("sub_element_quantity").value);
        const sub_element_quantity_default = document.getElementById("sub_element_quantity_value").value;

        document.getElementById("id_items-TOTAL_FORMS").value = n + 1;

        const newRow = createTableRow(n, category_id, category, purchase_price, quantity, sub_element_quantity, sub_element_quantity_default);
        document.querySelector('#items').prepend(newRow);

        document.getElementById("response").innerHTML = "";

        const element = document.getElementById(`id_items-${n}-DELETE`);
        if (element) {
            element.addEventListener('change', () => {
                const parentTr = element.closest('tr');
                if (parentTr) {
                    parentTr.style.display = element.checked ? 'none' : '';
                }
            });
        }

        const calculateTotalPrice = () => {
            const price = document.getElementById(`id_items-${n}-DELETE_total_price`);
            const subElementQuantity = document.getElementById(`id_items-${n}-sub_element_quantity`);
            const defaultSubElementQuantity = document.getElementById(`id_items-${n}-category_sub_element_quantity`);
            const quantity = document.getElementById(`id_items-${n}-quantity`);
            const purchasePrice = document.getElementById(`id_items-${n}-purchase_price`);
            price.value = Math.round((  subElementQuantity.value/defaultSubElementQuantity.value) 
                * purchasePrice.value * quantity.value * 100) / 100;
            all_total_price();
        };

        calculateTotalPrice();

        const elementsToWatch = [
            `id_items-${n}-sub_element_quantity`,
            `id_items-${n}-category_sub_element_quantity`,
            `id_items-${n}-quantity`,
            `id_items-${n}-purchase_price`
        ];

        elementsToWatch.forEach(id => {
            document.getElementById(id).onchange = calculateTotalPrice;
        });



    } catch (error) {
        document.getElementById("response").innerHTML = "ليس هناك شئ لتضيفه";
    }
}




