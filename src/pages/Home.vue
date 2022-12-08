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
const PSD = require('psd.js')
function _onExcute() {
	const orders: OrderInfo[] = sheetValues.value
	exportPng(orders[0])
}

const exportPng = async (order: OrderInfo) => {
	const files = templateFiles.value
	console.log(files)
	console.log(order.sku)
	const file = files[0]
	const psd = PSD.fromFile(file.path)
	psd.parse()
	const layer = psd.active
	console.log(psd.tree().export())
	await psd.image.saveAsPng(`./output/${order.id}.png`)
}

const _onRunPython = () => {
	PyScript.changeTextPyScript('change_text')
}

</script>

<template>
	<div class="container">
		<div class="template">
			<v-file-input label="Template folder" webkitdirectory v-model="templateFiles"></v-file-input>
			<v-table fixed-header height="300px">
				<tbody>
					<tr v-for="item in templateFiles">
						<td>{{ item.name }}</td>
					</tr>
				</tbody>
			</v-table>
		</div>
		<div class="order">
			<v-file-input label="Order files" v-model="selectedXmlFile"></v-file-input>
			<p>{{ xlsxMessage }}</p>
			<v-table fixed-header height="300px">
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
	<div id="#psd-output"></div>
	<v-btn v-on:click="_onExcute">
		Excute
	</v-btn>
	<v-btn @click="_onRunPython">
		Run Python
	</v-btn>
</template>

<style>
.container {
	display: flex;
	flex-direction: row;
}

.template {
	width: 400px;
}

.order {
	flex: 1
}
</style>