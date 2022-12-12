<script setup lang="ts">
import PyScript from '@/utilities/python'
import Excel from 'exceljs'
import fs from 'fs'
import { computed, ref, watch } from 'vue'
const templateFiles = ref<any[]>([])
const selectedXmlFile = ref<any[]>([])

watch(templateFiles, (newVal, oldVal) => {
	console.log(newVal)
})
type Cells = string[]
type OrderInfo = {
	id: string
	sku: string
	customName: string
}

const xlsxMessage = ref('')
const xmlFile = computed(() => selectedXmlFile.value[0])
const sheetValues = ref<OrderInfo[]>([])

watch(xmlFile, async (newValue, oldValue) => {
	xlsxMessage.value = `Reading ${newValue.name}`
	try {
		console.log(newValue.path)
		const workbook = new Excel.Workbook()
		const data = await fs.promises.readFile(newValue.path)
		await workbook.xlsx.load(data.buffer)
		const values = workbook.worksheets[0].getSheetValues() as Cells[]
		let newItems: OrderInfo[] = []
		values.forEach((value, ind) => {
			if (ind > 1) {
				const orderRaw = value.filter(val => (val.length > 0))
				const info: OrderInfo = {
					id: orderRaw[0],
					sku: orderRaw[1],
					customName: orderRaw[2]
				}
				newItems.push(info)
			}
		})
		sheetValues.value = newItems
	} catch (err) {
		xlsxMessage.value = `${err}`
	}

})

const treeData = ref('')
function _onExcute() {
	_onRunPython()
}

const exportPng = async (order: OrderInfo) => {
	const files = templateFiles.value
	console.log(files)
	console.log(order.sku)
	const file = files[0]
}

const _onRunPython = () => {
	const orders = sheetValues.value
	let files: { [key: string]: { ids: string[], texts: string[] } } = {}
	orders.forEach(val => {
		const current = files[val.sku] ?? { ids: [], texts: [] }
		files[val.sku] = {
			ids: [...current.ids, val.id],
			texts: [...current.texts, val.customName]
		}
	})
	Object.keys(files).forEach(id => {
		const file = templateFiles.value.find(val => val.name === `${id}.psd`)
		if (file) {
			PyScript.changeTextPyScript('change_text', [file.path, files[id].ids, files[id].texts])
		}
	})
}

</script>

<template>
	<div class="container">
		<div class="template">
			<v-file-input label="Template folder" hide-details small-chips webkitdirectory v-model="templateFiles"
				accept=".psd" hide-input show-size chips multiple></v-file-input>
			<v-table fixed-header style="flex: 1; max-height: fit-content;">
				<tbody>
					<tr v-for="item in templateFiles">
						<td>{{ item.name }}</td>
					</tr>
				</tbody>
			</v-table>
		</div>
		<div class="order">
			<v-file-input label="Order files" v-model="selectedXmlFile"
				accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"></v-file-input>
			<p>{{ xlsxMessage }}</p>
			<v-table fixed-header style="flex: 1; max-height: fit-content;">
				<thead>
					<tr>
						<th class="text-center">
							Order name
						</th>
						<th class="text-center">
							Sku template
						</th>
						<th class="text-center">
							Custom Name
						</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="item in sheetValues">
						<td>{{ item.id }}</td>
						<td>{{ item.sku }}</td>
						<td>{{ item.customName }}</td>
					</tr>
				</tbody>
			</v-table>
		</div>
	</div>
	<div>
		<v-btn v-on:click="_onExcute">
			Chạy
		</v-btn>
		<!-- <v-btn @click="_onRunPython">
			Testing
		</v-btn> -->
	</div>
</template>

<style>
.container {
	display: flex;
	flex-direction: row;
	height: 600px;
}

.template {
	width: 400px;
	flex: 1
}

.order {
	flex: 1
}
</style>